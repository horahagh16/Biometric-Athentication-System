import cv2
import numpy
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize, thin
import hashlib
import cv2
import numpy
from skimage.morphology import skeletonize
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
from deepface import DeepFace

# Encryption
def key_expansion(key):
    """Expand the variable-length key into a fixed-length 256-bit key using SHA-256."""
    hash_obj = hashlib.sha256()
    hash_obj.update(key.encode('utf-8'))
    return hash_obj.digest()

def generate_iv(key, plaintext):
    """Generate an IV using the first 8 bytes of the key and first 8 bytes of the plaintext."""
    if len(key) < 8 or len(plaintext) < 8:
        raise ValueError("Key and plaintext must be at least 8 bytes long.")

    iv_key_part = key[:7].encode('utf-8')  # Convert the first 8 bytes of key to bytes
    iv_plaintext_part = plaintext[:7]      # First 8 bytes of plaintext

    return iv_key_part + b'IV' + iv_plaintext_part

def compress_256_to_128(data):
    """Compress 256 bits to 128 bits using XOR."""
    # Split data into two 128-bit parts
    part1 = data[:16]
    part2 = data[16:]

    # XOR the two parts
    compressed = bytes(a ^ b for a, b in zip(part1, part2))
    return compressed

def encrypt_aes_cbc(plaintext, key):
    """Encrypt data using AES in CBC mode with a specific IV."""
    # Ensure plaintext is 256 bits
    if len(plaintext) != 32:
        raise ValueError("Plaintext must be 256 bits (32 bytes) long.")

    # Ensure key length is at least 13 characters
    if len(key) < 13:
        raise ValueError("Key must be at least 13 characters long.")

    # Expand the key to 256 bits
    expanded_key = key_expansion(key)

    # Generate IV from first 8 bytes of key and plaintext
    iv = generate_iv(key, plaintext)

    # Create AES cipher in CBC mode with the specific IV
    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)

    # Encrypt the plaintext
    encrypted_data = cipher.encrypt(pad(plaintext, AES.block_size))

    # Return the 128 bits (16 bytes) of the encrypted data
    return compress_256_to_128(encrypted_data)

# Fingerprint 
def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    img = numpy.array(img, dtype=numpy.uint8)
    # Threshold
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # Normalize to 0 and 1 range
    img[img == 255] = 1

    # Thinning
    skeleton = skeletonize(img)
    skeleton = numpy.array(skeleton, dtype=numpy.uint8)
    # Harris corners
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125
    # Extract keypoints
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
    # Define descriptor
    orb = cv2.ORB_create()
    # Compute descriptors
    _, des = orb.compute(img, keypoints)

    # Convert descriptors to a string
    if des is not None:
        descriptors_str = ' '.join(map(str, des.flatten()))
    else:
        descriptors_str = ''

    return descriptors_str

# Face 
def face_analyzer(img):
    # Load image and analyze
    objs = DeepFace.analyze(
        img_path=img,
        actions=("emotion", "gender", "race"),
        enforce_detection=False,
        detector_backend="retinaface",
    )

    # Extract relevant information
    dominant_emotion = objs[0]['dominant_emotion']
    dominant_gender = objs[0]['dominant_gender']
    dominant_race = objs[0]['dominant_race']

    # Concatenate into a single string
    result = f"{dominant_emotion}{dominant_gender}{dominant_race}"

    return result

# Execution
face_path = input('Face Picture Path:')
finger_path = input('Fingerprint Picture Path:')
key = input('Passphrase (at least 13 char):')

face_analysis_result = face_analyzer(face_path)
img1 = cv2.imread(finger_path, cv2.IMREAD_GRAYSCALE)
finger_analysis_result = get_descriptors(img1)

processed_biometric = face_analysis_result + finger_analysis_result

# Compute SHA-256 hash of the concatenated string
sha256_hash = hashlib.sha256(processed_biometric.encode()).digest()

plaintext = sha256_hash   # 256-bit input (32 bytes)

encrypted_data = encrypt_aes_cbc(plaintext, key)