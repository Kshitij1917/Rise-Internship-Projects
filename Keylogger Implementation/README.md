# 🔐 Keylogger (Educational Use Only)

## 📌 Objective
To understand how keyloggers operate to develop better security practices and defensive mechanisms.

## ⚠️ Ethical Use Disclaimer
This tool is **strictly for ethical and educational use**. Do not use this on any device or network without explicit permission.

## 🛠️ Requirements
- Python 3.x
- pynput library

## 📦 Installation
```bash
pip install pynput
```

## 🚀 How to Run
```bash
python keylogger.py
```

To stop recording, press the `ESC` key.

## 📁 Output
All keystrokes are logged to a timestamped file in the `logs/` directory.

## 🛡️ Antivirus Awareness Feature
This project includes a process scanner that checks for running antivirus software (e.g., Windows Defender, Kaspersky, Avast) to **raise awareness about malware detection** and demonstrate how keyloggers are often flagged and neutralized by AV solutions.

⚠️ This scan is non-invasive and reads only visible process names. It does **not bypass, disable, or interfere** with antivirus software in any way.
