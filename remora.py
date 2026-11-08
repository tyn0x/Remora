#!/usr/bin/env python3
import sys
import subprocess

CYAN = "\033[96m"
GREEN = "\033[92m" 
YELLOW = "\033[93m" 
RED = "\033[91m"
RESET = "\033[0m"

print(CYAN + r"""
  ____  _____ __  __  ___  ____     _    
 |  _ \| ____|  \/  |/ _ \|  _ \   / \   
 | |_) |  _| | |\/| | | | | |_) | / _ \  
 |  _ <| |___| |  | | |_| |  _ < / ___ \ 
 |_| \_\_____|_|  |_|\___/|_| \_/_/   \_\
 
  ><(((º> ---[pcap]   v0.2 | by tyn0x
==========================================
""" + RESET)

if len(sys.argv)<2:
	print(RED + "[!] ERROR: Missing .pcap file argument." + RESET)
	sys.exit()

archivo = sys.argv[1]
print(GREEN + "[+] Analyzing capture file:" + RESET)
print(archivo)

print(CYAN + "\n === IP CONVERSATIONS ===" + RESET)
command_ips = ["tshark", "-r", archivo, "-q", "-z", "conv,ip"]
subprocess.run(command_ips) 

print(CYAN + "\n === DETECTED DNS QUERIES ===" + RESET)
command_dns = ["tshark", "-r", archivo, "-Y", "dns", "-T", "fields", "-e", "ip.src", "-e", "dns.qry.name"] 
resultado_dns = subprocess.run(command_dns, capture_output=True, text=True)


if resultado_dns.stdout == "":
	print("[-] No DNS queries detected in this capture.")
else:
        print(resultado_dns.stdout)

print(CYAN + "\n === CREDENTIAL HUNTER (HTTP POST) ===" + RESET)
command_post = ["tshark", "-r", archivo, "-Y", 'http.request.method == "POST"', "-T", "fields", "-e", "ip.src", "-e", "text"] 
resultado_post = subprocess.run(command_post, capture_output=True, text=True)

if resultado_post.stdout == "":
        print("[-] No HTTP POST requests detected in this capture.")
else:
        print(YELLOW + "[!] Form payload data found:" + RESET)
        print(resultado_post.stdout)

print(CYAN + "\n === AUTOMATED SECRET ALERTS ===" + RESET)
if "FLAG" in resultado_dns.stdout:
        print(RED + "[!!!] RED ALERT: Hidden FLAG detected in DNS traffic!" + RESET)
if "password" in resultado_post.stdout:
        print(RED + "[!!!] RED ALERT: Exposed PASSWORD detected in HTTP POST!" + RESET) 
if "FLAG" in resultado_post.stdout:
        print(RED + "[!!!] RED ALERT: Hidden FLAG detected in HTTP POST!" + RESET)
