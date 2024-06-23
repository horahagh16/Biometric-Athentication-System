import numpy as np
import hashlib
from skimage.morphology import skeletonize
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def key_expansion(key):
    """Expand the variable-length key into a fixed-length 256-bit key using SHA-256."""
    hash_obj = hashlib.sha256()
    hash_obj.update(key.encode('utf-8'))
    return hash_obj.digest()

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

    # Create AES cipher in CBC mode with the specific IV
    cipher = AES.new(expanded_key, AES.MODE_CBC, 'iv')

    # Encrypt the plaintext
    encrypted_data = cipher.encrypt(pad(plaintext, AES.block_size))

    # Return the 128 bits (16 bytes) of the encrypted data
    return compress_256_to_128(encrypted_data)


plaintext = b'abcdefghijklmnopqrstuvwxyz123456'  # 256-bit input (32 bytes)
key = "this_is_a_secure_key"  # Key with at least 13 characters

encrypted_data = encrypt_aes_cbc(plaintext, key)
print("Encrypted data (128-bit):", encrypted_data.hex())
