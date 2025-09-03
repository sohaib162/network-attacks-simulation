# Research‑Only Security Tools (README)

> **Purpose:** This repository contains proof‑of‑concept scripts for studying common attack patterns **inside a controlled lab**. They are provided **exclusively for legal, research, and defensive education**. Do **not** run them on any system or network you do not own or lack **written authorization** to test.

> **You are responsible for compliance** with applicable laws and policies. Misuse may violate computer‑misuse laws (e.g., CFAA/CMA) and organizational policies.

---

## Contents

- `arp_mitm_full.py` — ARP spoofing / Man‑in‑the‑Middle (MITM) demonstration
- `ddos.py` — UDP flood traffic generator (simple)
- `mirai_udpplain_sim.py` — Mirai‑style UDP "udpplain" traffic simulator
- `ssh_bruteforce.py` — SSH login brute‑force demonstration (Paramiko)
- `web_bruteforce.py` — Web login brute‑force demonstration (requests)

Each script is intended to help blue‑teamers and students **recognize** patterns, measure detections, and validate defenses **in a lab**.

---

## Who This Is For

- Security researchers, SOC/blue‑team analysts, and students conducting **authorized** lab exercises.
- Red teams operating under a **written rules‑of‑engagement** (ROE) with explicit scope.

---

## Safety, Ethics, and Scope (Read First)

1. **Authorization:** Obtain written permission (or limit strictly to your own lab assets).
2. **Isolation:** Use an **air‑gapped** or **host‑only** lab network (e.g., VirtualBox Host‑Only, VMware Private LAN, or a separate Wi‑Fi router not connected to the Internet).
3. **Non‑production targets:** Exercise only against **disposable lab VMs/containers** you control.
4. **Rate limiting:** For traffic generators, keep packet rates low and time‑boxed; monitor CPU/IO.
5. **Logging:** Enable packet capture (e.g., tcpdump/Wireshark) and host logs to study results.
6. **Cleanup:** Restore ARP tables, disable IP forwarding, and tear down lab resources after use.
7. **Data privacy:** Never capture or store real user data.

---

## Recommended Lab Setups

You can use **either** of the following isolation approaches:

### Option A — Two or Three Local VMs (easiest to reason about)
- **Tools:** VirtualBox/VMware/Hyper‑V.
- **Network:** Create a **Host‑Only** network (no Internet). Place VMs on the same subnet.
- **Roles:**
  - `victim` VM (Linux),
  - `gateway` VM (Linux) or just another host,
  - optional `attacker` VM (Linux) where you run these scripts.
- **Visibility:** Use tcpdump/Wireshark on the attacker VM to observe traffic and verify detections on the victim/gateway VMs.

### Option B — Containers on an Isolated Bridge Network (developer‑friendly)
- **Tools:** Docker or Podman.
- **Network:** Create a custom bridge network and do **not** publish ports to the host or Internet.
- **Notes:** Some L2 behaviors (like ARP) can be abstracted in container networks; prefer VMs for ARP MITM accuracy. Use containers for the SSH/Web targets to practice safe brute‑force handling.

---

## Environment Preparation

1. **Python**: 3.10+ recommended.
2. **Virtual environment** (recommended):
   ```bash
   python -m venv .venv && source .venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -U pip
   pip install scapy paramiko requests
   ```
4. **System capabilities** (Linux): raw sockets & packet forwarding require root/admin. Prefer running in a **dedicated lab VM** with sudo.
5. **Targets for Safe Testing**:
   - **SSH target**: a lab Linux VM with a **dedicated test account** and known credentials.
   - **Web target**: a local, purposely vulnerable practice app (e.g., a **test** login page you created for this lab). Do **not** point at real apps.
   - **Traffic capture**: run `tcpdump` / Wireshark to observe artifacts.

> **Never** point these scripts at production, Internet hosts, or systems outside your explicit scope.

---

## Using the Scripts Responsibly

Below is **high‑level, lab‑only** guidance to help you prepare scenarios and understand expected artifacts. Replace any example IPs with your **lab subnet addresses** only.

### 1) `arp_mitm_full.py` — ARP Spoofing / MITM (Lab‑Only)

**What it demonstrates**  
Poisons ARP caches of two hosts so traffic is routed via the attacker (common L2 MITM technique).

**Prepare the lab**
- Place `attacker`, `victim`, and `gateway/peer` on the **same L2 segment** in your host‑only lab.
- Ensure you have permission and that these are **non‑production** VMs.

**Safe usage notes**
- The script enables IP forwarding and periodically sends spoofed ARP replies.
- Stop with `Ctrl+C` to trigger the built‑in ARP restoration routine.
- Observe: ARP tables on `victim` and `gateway` show attacker’s MAC for the peer; PCAPs show relayed traffic.

**Defensive learning goals**
- Validate ARP spoofing detections (e.g., Gratuitous ARP anomalies, MAC/IP conflicts).
- Confirm network segmentation and DHCP snooping/DAI effectiveness.

### 2) `ddos.py` — UDP Flood Generator (Lab‑Only)

**What it demonstrates**  
Generates sustained UDP traffic toward a target host/port to study rate‑based controls and logging.

**Prepare the lab**
- Use a disposable lab host as the target, ideally throttled by a host firewall or traffic shaper.
- Keep durations short and rates modest to avoid resource exhaustion.

**Safe usage notes**
- Intended for observing telemetry (e.g., NetFlow, conntrack, host CPU) under load in a lab.
- Do not point at any real or unauthorized service.

**Defensive learning goals**
- Tune rate‑limits, IDS signatures, and alerts for volumetric UDP flows.

### 3) `mirai_udpplain_sim.py` — Mirai‑Style UDP Traffic (Lab‑Only)

**What it demonstrates**  
A simplified version of Mirai’s `udpplain` pattern (often empty UDP payloads, randomized ports).

**Prepare the lab**
- Same as `ddos.py`, but ensure **strict isolation** due to high packet rates.
- Consider dramatically reducing `PACKET_RATE` for safe testing.

**Defensive learning goals**
- Study signatures/heuristics for Mirai‑like bursts and randomized‑port floods.

### 4) `ssh_bruteforce.py` — SSH Brute‑Force (Lab‑Only)

**What it demonstrates**  
Credential‑stuffing and password‑guessing behavior against SSH.

**Prepare the lab**
- Stand up an SSH server **you own** with a **dedicated test user** and strong lockout policy.
- Ensure you have explicit permission to run authentication tests.

**Safe usage notes**
- Keep the password list to **nonsensitive test values**.
- Validate lockout, fail2ban, audit logs, and alerting.

**Defensive learning goals**
- Confirm SSH hardening: key‑only auth, 2FA, backoff, and alerting on repeated failures.

### 5) `web_bruteforce.py` — Web Login Brute‑Force (Lab‑Only)

**What it demonstrates**  
Automated password guessing against a login form.

**Prepare the lab**
- Use a local **practice** web app with a dummy account. Never target real apps.
- Ensure the app displays clear failure messages you can safely test against.

**Safe usage notes**
- Verify rate‑limits, CAPTCHA, lockout, and WAF rules in the lab.

**Defensive learning goals**
- Tune detections for repeated login failures and unusual IP/user‑agent patterns.


---

## Measurement & Documentation Tips

- Record: date/time, targets (lab identifiers), configs, and packet rates.
- Save PCAPs and host logs. Capture CPU/RAM/network counters during tests.
- Note which detections fired (IDS/EDR/NDR/SIEM) and any false positives.
- Keep runs **short** and **repeatable**.

---

## Cleanup Checklist

- Stop running scripts; allow ARP restoration to complete (`arp_mitm_full.py` does this on `Ctrl+C`).
- Disable IP forwarding if you enabled it for the demo.
- Revert any lab firewall or authentication policy changes.
- Tear down lab VMs/containers or revert to clean snapshots.

---

## Final Reminder

These scripts are **education and research tools** only. Keep activities within **explicitly authorized scope**, capture evidence for learning, and prioritize safety at all times.

