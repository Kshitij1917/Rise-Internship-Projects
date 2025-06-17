
import csv
from plyer import notification

def export_to_csv(networks, filename):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["SSID", "Signal", "Channel", "Security"])
        writer.writeheader()
        for net in networks:
            writer.writerow(net)

def notify_new_networks(new_networks):
    if not new_networks:
        return
    names = ', '.join([net['SSID'] for net in new_networks])
    notification.notify(
        title="🔔 New Wi-Fi Network(s) Detected",
        message=f"{names}",
        timeout=5
    )
