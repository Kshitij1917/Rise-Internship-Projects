import socket
import threading
import json
import os
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from colorama import Fore, init
from twilio.rest import Client

init(autoreset=True)

open_ports = []
vuln_db = {}
critical_alerts = []

def load_vulnerability_database():
    global vuln_db
    if not os.path.exists("vuln_data.json"):
        print(f"{Fore.RED}[-] Vulnerability database not found.")
        return
    with open("vuln_data.json", "r") as f:
        vuln_db = json.load(f)

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                service = socket.getservbyport(port, "tcp") if port < 1024 else "unknown"
                print(f"{Fore.GREEN}[+] Port {port} is open ({service})")
                open_ports.append((port, service))
    except Exception as e:
        pass

def scan_ports(ip, ports):
    print(f"{Fore.CYAN}[*] Scanning {ip} for open ports...")
    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def generate_vulnerability_report(vuln_db):
    print(f"{Fore.MAGENTA}\n[+] Vulnerability Report:")
    for port, service in open_ports:
        if str(port) in vuln_db:
            vuln_info = vuln_db[str(port)]
            severity = vuln_info.get("severity", "unknown")
            print(f"{Fore.YELLOW}- Port {port} ({service}): {vuln_info['vulnerability']} [{severity}]")
            if severity.lower() == "critical":
                critical_alerts.append((port, service, vuln_info['vulnerability']))
        else:
            print(f"- Port {port} ({service}): No known vulnerabilities")

def send_email_alert(critical_alerts, max_retries=3):
    if not os.path.exists("config.json"):
        print(f"{Fore.RED}[-] Missing config.json for email settings.")
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    sender = config["sender_email"]
    password = config["app_password"]
    recipients = config["receiver_emails"]

    subject = "🚨 Critical Vulnerabilities Detected on Scanned Host"
    body = "The following critical issues were found:\n\n"
    for port, service, vuln in critical_alerts:
        body += f"- Port {port} ({service}): {vuln}\n"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    for attempt in range(1, max_retries + 1):
        try:
            print(f"{Fore.CYAN}[i] Attempt {attempt}: Sending email alert...")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            print(f"{Fore.GREEN}[+] Email alert sent to: {', '.join(recipients)}")
            return
        except Exception as e:
            print(f"{Fore.RED}[-] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                wait_time = 5 * attempt
                print(f"{Fore.YELLOW}[i] Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"{Fore.RED}[-] All attempts to send email failed.")

def send_sms_alert(critical_alerts):
    if not os.path.exists("config.json"):
        print(f"{Fore.RED}[-] Missing config.json for SMS settings.")
        return

    with open("config.json", "r") as f:
        config = json.load(f)

    sid = config["twilio_account_sid"]
    token = config["twilio_auth_token"]
    from_number = config["twilio_from_number"]
    to_number = config["twilio_to_number"]

    body = "CRITICAL Ports:\n"
    for port, service, vuln in critical_alerts:
        body += f"{port}-{service}\n"

    body = body[:160]

    try:
        client = Client(sid, token)
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to_number
        )
        print(f"{Fore.GREEN}[+] SMS alert sent: SID {message.sid}")
    except Exception as e:
        print(f"{Fore.RED}[-] SMS failed: {e}")

def main():
    target = input("Enter IP address to scan: ")
    ports = range(1, 1025)
    load_vulnerability_database()
    scan_ports(target, ports)
    generate_vulnerability_report(vuln_db)
    if critical_alerts:
        send_email_alert(critical_alerts)
        send_sms_alert(critical_alerts)

if __name__ == "__main__":
    main()
