import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Input and output paths
ENCRYPTED_FILE = Path("encrypted_seed.txt")
OUTPUT_FILE = Path("seed.txt")
PRIVATE_KEY_FILE = Path("student_private.pem")


def decrypt_seed():
    # 1. Read encrypted seed from file
    encrypted_b64 = ENCRYPTED_FILE.read_text().strip()

    # Base64 decode it
    encrypted_bytes = base64.b64decode(encrypted_b64)

    # 2. Load private key
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY_FILE.read_bytes(),
        password=None
    )

    # 3. Decrypt using RSA + OAEP + SHA256
    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )
    )

    # 4. Convert bytes → text
    seed_hex = decrypted_bytes.decode()

    # 5. Validate 64-character hex string
    if len(seed_hex) != 64:
        raise ValueError("Seed is NOT 64 characters!")

    if any(c not in "0123456789abcdef" for c in seed_hex):
        raise ValueError("Seed contains invalid characters!")

    # 6. Save final seed
    OUTPUT_FILE.write_text(seed_hex)

    print("Decryption successful!")
    print("Seed saved to data/seed.txt")


if __name__ == "__main__":
    decrypt_seed()
