#!/usr/bin/env python3
import sys
import subprocess

print(r"""
  ____  _____ __  __  ___  ____     _    
 |  _ \| ____|  \/  |/ _ \|  _ \   / \   
 | |_) |  _| | |\/| | | | | |_) | / _ \  
 |  _ <| |___| |  | | |_| |  _ < / ___ \ 
 |_| \_\_____|_|  |_|\___/|_| \_/_/   \_\
 
  ><(((º> ---[pcap]   v0.1 | by tyn0x
==========================================
""")

if len(sys.argv)<2:
	print("[!]ERROR: Olvidaste adjuntar el archivo .pcap")
	sys.exit()

archivo = sys.argv[1]
print("[+] Vamos a analizar el archivo:")
print(archivo)

print("\n === CONVERSACIONES IP ===")
command_ips = ["tshark", "-r", archivo, "-q", "-z", "conv,ip"]
subprocess.run(command_ips) 

print("\n === CONSULTAS DNS DETECTADAS ===")
command_dns = ["tshark", "-r", archivo, "-Y", "dns", "-T", "fields", "-e", "ip.src", "-e", "dns.qry.name"] 
resultado_dns = subprocess.run(command_dns, capture_output=True, text=True)


if resultado_dns.stdout == "":
	print("[-] No se detectaron consultas DNS en este archivo.")
else:
        print(resultado_dns.stdout)

print("\n === CAZADOR DE CREDENCIALES (HTTP POST) ===")
command_post = ["tshark", "-r", archivo, "-Y", 'http.request.method == "POST"', "-T", "fields", "-e", "ip.src", "-e", "text"] 
resultado_post = subprocess.run(command_post, capture_output=True, text=True)

if resultado_post.stdout == "":
        print("[-] No se detectaron envios HTTP POST en este archivo.")
else:
        print("[!] Datos enviados en formularios encontrados:")
        print(resultado_post.stdout)

print("\n === ALERTA AUTOMATICA DE SECRETOS ===")
if "FLAG" in resultado_dns.stdout:
        print("[!!!] ALERTA ROJA: Se encontro una FLAG oculta en el trafico DNS!")
if "password" in resultado_post.stdout:
        print("[!!!] ALERTA ROJA: Se encontro un PASSWORD expuesto en HTTP POST!") 
if "FLAG" in resultado_post.stdout:
        print("[!!!] ALERTA ROJA: Se encontro una FLAG oculta en HTTP POST!")
