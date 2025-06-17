
import os
from cryptography.fernet import Fernet

def load_key():
    return open("key.key", "rb").read()

def decrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    try:
        decrypted_data = Fernet(key).decrypt(data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"🔓 Decrypted: {file_path}")
    except Exception as e:
        print(f"❌ Failed to decrypt {file_path}: {e}")

def decrypt_folder(folder_path, key):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)

if __name__ == "__main__":
    folder_to_decrypt = "sample_files"
    key = load_key()
    decrypt_folder(folder_to_decrypt, key)
    print("\n✅ All files decrypted.")
