
# Simple Ransomware Simulator (Educational Only)

This Python tool simulates ransomware behavior:
- Encrypts files in a directory using Fernet symmetric encryption.
- Decrypts only with the correct key stored in `key.key`.

## Usage
1. Place files to encrypt inside `sample_files/`.
2. Run `encryptor.py` to encrypt files.
3. Run `decryptor.py` to decrypt files using the saved key.

## WARNING
This tool is for educational purposes only.
Do NOT use it to encrypt unauthorized data or real systems.

🛠 Requirements
Install the required Python module:

pip install cryptography
🧪 Test Instructions
# Encrypt
python encryptor.py

# Decrypt
python decryptor.py
