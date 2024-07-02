import cv2
import numpy as np
from skimage.morphology import skeletonize
import hashlib

def get_descriptors(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img = clahe.apply(img)
    img = np.array(img, dtype=np.uint8)
    # Threshold
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # Normalize to 0 and 1 range
    img[img == 255] = 1

    # Thinning
    skeleton = skeletonize(img)
    skeleton = np.array(skeleton, dtype=np.uint8)
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

img1 = cv2.imread('102_1.tif', cv2.IMREAD_GRAYSCALE)
des1 = get_descriptors(img1)

# Concatenate keypoints into a single string
keypoints_str = ' '.join([f"({des.pt[0]}, {des.pt[1]})" for des in des1])

# Compute SHA-256 hash of the concatenated keypoints string
sha256_hash = hashlib.sha256(keypoints_str.encode()).hexdigest()

print(sha256_hash)