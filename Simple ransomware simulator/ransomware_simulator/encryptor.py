
import os
from cryptography.fernet import Fernet

print("⚠️ WARNING: This is an educational tool only. Do NOT use this on real or sensitive data.")

def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open("key.key", "rb").read()

def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    encrypted_data = Fernet(key).encrypt(data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)

def encrypt_folder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)
            print(f"🔒 Encrypted: {file_path}")

if __name__ == "__main__":
    folder_to_encrypt = "sample_files"
    key = generate_key()
    encrypt_folder(folder_to_encrypt, key)
    print("\n✅ All files encrypted. Store key.key securely for decryption.")
