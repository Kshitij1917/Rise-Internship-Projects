import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from crypto_utils import encrypt_message, decrypt_message

# Replace with your server's IP if over LAN
HOST = 'localhost'  # e.g., '192.168.1.50'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive the public key from server
public_key = client.recv(4096)

# Ask user to login or register
action = simpledialog.askstring("Action", "Type LOGIN or REGISTER:")
if action not in ["LOGIN", "REGISTER"]:
    messagebox.showerror("Error", "Invalid option. Must be LOGIN or REGISTER.")
    exit()

username = simpledialog.askstring("Username", "Enter username:")
password = simpledialog.askstring("Password", "Enter password:", show="*")

# Send credentials
client.send(action.encode())
client.send(username.encode())
client.send(password.encode())

# Receive and handle server response
status = client.recv(1024).decode()

if status == "REGISTER_FAILED":
    messagebox.showerror("Registration Failed", "Username already exists.")
    exit()
elif status == "AUTH_FAILED":
    messagebox.showerror("Login Failed", "Invalid username or password.")
    exit()
elif status == "REGISTER_SUCCESS":
    messagebox.showinfo("Registered", "Registration successful! You are now logged in.")
elif status == "AUTH_SUCCESS":
    messagebox.showinfo("Welcome", "Login successful!")
else:
    messagebox.showerror("Error", "Unknown server response.")
    exit()

# GUI setup
window = tk.Tk()
window.title("Secure Chat")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled', height=20, width=50)
chat_area.pack(padx=10, pady=10)

msg_entry = tk.Entry(window, width=40)
msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

def send_message():
    msg = msg_entry.get()
    if msg:
        encrypted = encrypt_message(public_key, msg)
        client.send(encrypted.encode())
        msg_entry.delete(0, tk.END)

send_btn = tk.Button(window, text="Send", command=send_message)
send_btn.pack(side=tk.LEFT, padx=10, pady=(0, 10))

def receive_messages():
    while True:
        try:
            data = client.recv(4096).decode()
            decrypted = decrypt_message(public_key, data)
            chat_area.config(state='normal')
            chat_area.insert(tk.END, decrypted + '\n')
            chat_area.yview(tk.END)
            chat_area.config(state='disabled')
        except:
            break

threading.Thread(target=receive_messages, daemon=True).start()
window.mainloop()
