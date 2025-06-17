
import pywifi
from pywifi import const
import time

def get_interface():
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if not interfaces:
        raise Exception("No Wi-Fi interface found.")
    return interfaces[0]

def scan_wifi():
    iface = get_interface()
    iface.scan()
    time.sleep(2)
    results = iface.scan_results()

    networks = []
    seen = set()

    for net in results:
        if net.ssid not in seen:
            seen.add(net.ssid)
            networks.append({
                "SSID": net.ssid,
                "Signal": net.signal,
                "Channel": convert_freq_to_channel(net.freq),
                "Security": get_security_type(net.akm)
            })

    return sorted(networks, key=lambda x: x["Signal"], reverse=True)

def get_security_type(akm):
    if not akm:
        return "Open"
    if const.AKM_TYPE_WPA2 in akm:
        return "WPA2"
    if const.AKM_TYPE_WPA in akm:
        return "WPA"
    return "Unknown"

def convert_freq_to_channel(freq):
    if 2412 <= freq <= 2472:
        return (freq - 2407) // 5
    elif freq == 2484:
        return 14
    elif 5180 <= freq <= 5825:
        return (freq - 5000) // 5
    else:
        return "?"
