# test_totp.py
from pathlib import Path
from totp_utils import generate_totp_code, verify_totp_code

# Read your hex seed from data/seed.txt
seed_path = Path("seed.txt")
if not seed_path.exists():
    print("Error: data/seed.txt not found. Run Step 5 first to create it.")
    exit(1)

hex_seed = seed_path.read_text().strip()

print("Hex seed (from file):", hex_seed)

# Generate TOTP
code = generate_totp_code(hex_seed)
print("Current TOTP:", code)

# Verify the code we just generated (should be True)
print("Verify generated code:", verify_totp_code(hex_seed, code))

# Test verify wrong code (should be False)
print("Verify wrong code (000000):", verify_totp_code(hex_seed, "000000"))
