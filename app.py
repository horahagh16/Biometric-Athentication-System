from flask import Flask, request, jsonify, render_template
import os
import re
import cv2
import numpy as np
import hashlib
import shutil
from skimage.morphology import skeletonize
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from deepface import DeepFace

app = Flask(__name__)

# Encryption Functions
def key_expansion(key):
    """Expand the variable-length key into a fixed-length 256-bit key using SHA-256."""
    return hashlib.sha256(key.encode('utf-8')).digest()

def generate_iv(key, plaintext):
    """Generate an IV using the first 8 bytes of the key and first 8 bytes of the plaintext."""
    return key[:7].encode('utf-8') + b'IV' + plaintext[:7]

def compress_256_to_128(data):
    """Compress 256 bits to 128 bits using XOR operation on the two 128-bit halves."""
    return bytes(a ^ b for a, b in zip(data[:16], data[16:]))

def encrypt_aes_cbc(plaintext, key):
    """Encrypt data using AES in CBC mode with a specific IV."""
    expanded_key = key_expansion(key)  # Expand the key to 256 bits
    iv = generate_iv(key, plaintext)   # Generate IV from the key and plaintext
    cipher = AES.new(expanded_key, AES.MODE_CBC, iv)  # Initialize AES cipher in CBC mode
    encrypted_data = cipher.encrypt(pad(plaintext, AES.block_size))  # Encrypt the plaintext
    return compress_256_to_128(encrypted_data)  # Return the compressed 128-bit encrypted data

# Fingerprint Processing Function
def get_descriptors(img):
    """Process the fingerprint image to extract descriptors."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)  # Apply CLAHE for contrast enhancement
    img = np.array(img, dtype=np.uint8)
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)  # Thresholding
    img[img == 255] = 1  # Normalize to binary image
    skeleton = skeletonize(img)  # Skeletonize the image
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)  # Detect Harris corners
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125  # Threshold for detecting keypoints
    keypoints = [cv2.KeyPoint(y, x, 1) for x in range(harris_normalized.shape[0]) for y in range(harris_normalized.shape[1]) if harris_normalized[x][y] > threshold_harris]
    orb = cv2.ORB_create()  # Initialize ORB detector
    _, des = orb.compute(img, keypoints)  # Compute ORB descriptors
    return ' '.join(map(str, des.flatten())) if des is not None else ''  # Return descriptors as a string

# Face Processing Function
def face_analyzer(img):
    """Analyze the face image for emotion, gender, and race."""
    objs = DeepFace.analyze(img_path=img, actions=("emotion", "gender", "race"), enforce_detection=False, detector_backend="retinaface")
    return f"{objs[0]['dominant_emotion']}{objs[0]['dominant_gender']}{objs[0]['dominant_race']}"

# Common Functionality for Both Signup and Login
def process_biometrics(face_path, finger_path, key):
    """Process both face and fingerprint images, then encrypt the result."""
    face_analysis_result = face_analyzer(face_path)  # Analyze the face image
    img1 = cv2.imread(finger_path, cv2.IMREAD_GRAYSCALE)  # Read the fingerprint image
    finger_analysis_result = get_descriptors(img1)  # Get fingerprint descriptors
    processed_biometric = face_analysis_result + finger_analysis_result  # Concatenate face and fingerprint data
    sha256_hash = hashlib.sha256(processed_biometric.encode()).digest()  # Compute SHA-256 hash of the data
    encrypted_data = encrypt_aes_cbc(sha256_hash, key)  # Encrypt the hash
    checksum = hashlib.sha256(encrypted_data).digest()  # Compute checksum of the encrypted data
    first_4_bits = checksum[0] >> 4  # Extract the first 4 bits of the checksum
    encrypted_data_bits = ''.join(format(byte, '08b') for byte in encrypted_data)  # Convert encrypted data to binary string
    final_bit_string = encrypted_data_bits + format(first_4_bits, '04b')  # Append the first 4 bits to the binary string
    last_11_bits = final_bit_string[-11:]  # Extract the last 11 bits
    word_index = int(last_11_bits, 2)  # Convert the last 11 bits to an integer
    with open('english.txt', 'r') as f:  # Load word list
        wordlist = f.read().splitlines()
    return wordlist[word_index]  # Return the mnemonic word corresponding to the index

def valid_key(key):
    """Validate that the key contains at least one uppercase, lowercase, digit, and special character."""
    return (len(key) >= 13 and
            re.search(r'[A-Z]', key) and
            re.search(r'[a-z]', key) and
            re.search(r'\d', key) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', key))

def clear_uploads_folder():
    """Remove all files in the uploads folder."""
    folder = 'uploads'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # remove the file
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove a directory
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/process_biometrics', methods=['POST'])
def process_biometrics_request():
    process = request.form['process']
    face_image = request.files['faceImage']
    finger_image = request.files['fingerImage']
    passphrase = request.form['passphrase']
    
    if not valid_key(passphrase):
        return "Passphrase must be at least 13 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character.", 400
    
    face_path = os.path.join('uploads', face_image.filename)
    finger_path = os.path.join('uploads', finger_image.filename)
    
    face_image.save(face_path)
    finger_image.save(finger_path)
    
    if process == 'signup':
        mnemonic_word = process_biometrics(face_path, finger_path, passphrase)
        response = f"The mnemonic word: {mnemonic_word}"
    elif process == 'login':
        mnemonic = request.form['mnemonic']
        mnemonic_word = process_biometrics(face_path, finger_path, passphrase)
        if mnemonic == mnemonic_word:
            response = "WELCOME"
        else:
            response = "UNSUCCESSFUL AUTHENTICATION"
    else:
        return "Invalid process", 400
    
    clear_uploads_folder()
    return response


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
