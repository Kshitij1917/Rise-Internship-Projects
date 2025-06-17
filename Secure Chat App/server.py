import socket
import threading
import json
import os
from crypto_utils import generate_keys, decrypt_message, encrypt_message

USER_FILE = 'users.json'

# Load users from file or start with empty dict
if os.path.exists(USER_FILE):
    with open(USER_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

private_key, public_key = generate_keys()
clients = []

def client_thread(conn, addr):
    try:
        conn.send(public_key)

        # Login/Register flow
        try:
            action = conn.recv(1024).decode()
            username = conn.recv(1024).decode()
            password = conn.recv(1024).decode()
        except ConnectionResetError:
            print(f"[{addr}] disconnected during login/registration.")
            conn.close()
            return

        if action == "REGISTER":
            if username in users:
                conn.send("REGISTER_FAILED".encode())
                conn.close()
                return
            else:
                users[username] = password
                with open(USER_FILE, 'w') as f:
                    json.dump(users, f)
                conn.send("REGISTER_SUCCESS".encode())
                broadcast(f"Server: {username} has joined the chat.", None)

        elif action == "LOGIN":
            if users.get(username) != password:
                conn.send("AUTH_FAILED".encode())
                conn.close()
                return
            else:
                conn.send("AUTH_SUCCESS".encode())
                broadcast(f"Server: {username} has joined the chat.", None)

        clients.append(conn)

        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                decrypted = decrypt_message(private_key, data.decode())
                print(f"[{addr}]: {decrypted}")
                broadcast(f"{username}: {decrypted}", conn)
            except (ConnectionResetError, ConnectionAbortedError):
                print(f"[{addr}] forcibly disconnected.")
                break
            except Exception as e:
                print(f"[{addr}] Error: {e}")
                break

    finally:
        conn.close()
        if conn in clients:
            clients.remove(conn)

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                encrypted = encrypt_message(public_key, message)
                client.send(encrypted.encode())
            except:
                client.close()

def server_input_thread():
    while True:
        try:
            msg = input()
            if msg.strip():
                broadcast(f"Server: {msg}", None)
        except:
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Server started. Waiting for clients...")

    threading.Thread(target=server_input_thread, daemon=True).start()

    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=client_thread, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
