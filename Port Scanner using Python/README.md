# 🔍 Python Port Scanner with Vulnerability Alerts

A real-world Python-based port scanner with:
- Open port detection
- Vulnerability matching
- Email & SMS alerts (for critical issues)
- Retry logic for reliability

## 📦 Features

- Scans top 1024 TCP ports on a given IP
- Detects open ports using multithreading
- Matches against known vulnerabilities (`vuln_data.json`)
- Sends:
  - 📧 Email alerts (multi-recipient)
  - 📱 SMS alerts (via Twilio or Email-to-SMS)
- Retries failed email attempts (up to 3 tries)

## ⚙️ Setup

1. Rename `config.json.template` → `config.json`
2. Fill in:
   - Gmail: `sender_email`, `app_password`, `receiver_emails`
   - Twilio (for SMS): `account_sid`, `auth_token`, etc.

3. Install requirements:

```bash
pip install colorama twilio
```

## 🚀 Run

```bash
python port_scanner.py
```

Enter the target IP when prompted.

## 🔐 Security Notes

- Use [App Passwords](https://myaccount.google.com/apppasswords) for Gmail
- Do NOT commit `config.json` to version control
