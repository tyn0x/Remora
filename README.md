# 🐟 Remora (`v0.1`)

```text
  ____  _____ __  __  ___  ____     _    
 |  _ \| ____|  \/  |/ _ \|  _ \   / \   
 | |_) |  _| | |\/| | | | | |_) | / _ \  
 |  _ <| |___| |  | | |_| |  _ < / ___ \ 
 |_| \_\_____|_|  |_|\___/|_| \_/_/   \_\
 
  ><(((º> ---[pcap]   v0.1 | by tyn0x
==========================================
```

**Remora** is a lightweight, 100% local CLI network triage and PCAP intelligence tool written in Python.

Just like a remora fish attaches itself to a shark to feed on what passes by, **Remora** rides on top of **TShark** (`Wireshark` CLI) to automatically digest `.pcap` files, extract key network conversations, hunt for cleartext credentials, and alert on suspicious data leaks directly in your terminal.

---

## 💡 Motivation (Why I Built This)

While studying network traffic analysis and packet inspection, I noticed how common it is to use third-party online PCAP analyzers (like *Apackets*) to get quick visual summaries of a capture file.

However, **privacy over packet analysis is a big concern, and giving away your information in exchange for getting a nice format for it didn't look like a fair trade.** PCAP files often contain internal IP addresses, DNS queries, session tokens, and sensitive payloads.

I built **Remora** as my first Python security tool to get that same instant triage overview **100% offline and locally**, keeping full control of the data under the hood.

---

## ⚙️ Features (`v0.1`)

1. **IPv4 Conversation Matrix**: Automatically summarizes who is talking to whom, total frames, bytes transferred, and connection duration (`tshark -q -z conv,ip`).
2. **DNS Query Extractor**: Lists every source IP and the exact domain names requested (`dns.qry.name`) to spot C2 callbacks or DNS tunneling.
3. **Cleartext Credential Hunter (`HTTP POST`)**: Filters `POST` requests and extracts form payloads in ASCII to catch exposed usernames and passwords.
4. **Automated Secret & Flag Alerts**: Scans captured streams in memory and triggers high-priority alerts (`[!!!] ALERTA ROJA`) if sensitive strings (`password`, `FLAG`) are leaked in HTTP or DNS traffic.

---

## 🛠️ Requirements

- **Python 3.x** (uses only standard library modules: `sys` and `subprocess` — zero external `pip` dependencies).
- **TShark** (part of the Wireshark suite) installed and available in your system `PATH`.
  - **macOS (Homebrew)**: `brew install --cask wireshark`
  - **Linux (Debian/Ubuntu/Kali)**: `sudo apt install tshark`

---

## 🚀 Usage

Clone the repository and run `remora.py` passing any `.pcap` or `.pcapng` file as an argument:

```bash
python3 remora.py evidencia2.pcap
```

### Example Output

```text
  ____  _____ __  __  ___  ____     _    
 |  _ \| ____|  \/  |/ _ \|  _ \   / \   
 | |_) |  _| | |\/| | | | | |_) | / _ \  
 |  _ <| |___| |  | | |_| |  _ < / ___ \ 
 |_| \_\_____|_|  |_|\___/|_| \_/_/   \_\
 
  ><(((º> ---[pcap]   v0.1 | by tyn0x
==========================================

[+] Vamos a analizar el archivo:
evidencia2.pcap

 === CONVERSACIONES IP ===
================================================================================
IPv4 Conversations
Filter:<No Filter>
                                               |       <-      | |       ->      | |     Total     |    Relative    |   Duration   |
                                               | Frames  Bytes | | Frames  Bytes | | Frames  Bytes |      Start     |              |
192.168.10.25        <-> 10.0.0.80                  0 0 bytes        36 4712 bytes      36 4712 bytes     0.000000000        34.6443
================================================================================

 === CONSULTAS DNS DETECTADAS ===
[-] No se detectaron consultas DNS en este archivo.

 === CAZADOR DE CREDENCIALES (HTTP POST) ===
[!] Datos enviados en formularios encontrados:
192.168.10.25   Timestamps,POST /auth/login.php HTTP/1.1\r\n,\r\n,Form item: "username" = "admin_carlos",Form item: "password" = "FLAG{cleartext_http_post_exposes_passwords}",Form item: "submit" = "Login"

 === ALERTA AUTOMATICA DE SECRETOS ===
[!!!] ALERTA ROJA: Se encontro un PASSWORD expuesto en HTTP POST!
[!!!] ALERTA ROJA: Se encontro una FLAG oculta en HTTP POST!
```

---

## 🗺️ Roadmap (`v0.2+`)

As I continue expanding my Python and network forensics skills, here is what I am planning to implement next:

- [ ] **Color-based terminal outputs**: Implement ANSI color codes (green for normal info, yellow for warnings, and bright red for `[!!!]` secret/credential alerts) to make visual triage faster.
- [ ] **Extract images and hidden files**: Automatically carve and export files, images, and binaries transferred over HTTP/SMB streams (`tshark --export-objects`) into a local `extracted/` folder.
- [ ] **English CLI localization & custom keyword flags**: Allow passing custom search keywords from the command line.

---

## 👤 Author

Created by **tyn0x** as part of my hands-on journey into Cyber Security, packet analysis, and building custom CLI tools from scratch.
