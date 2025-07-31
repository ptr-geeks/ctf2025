from scapy.all import IP, UDP, Raw, wrpcap
import struct
import hashlib
import os

SERVER_SECRET = b"supersecret_server_flag_key"

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def generate_key(nonce):
    return hashlib.sha256(nonce + SERVER_SECRET).digest()[:4]

# Definicija podatkov
flag = b'ptr{dummy_flag}'
file_id = b'\x00\x00\x00\x02'
file_name = b'file_00000002'

# Simulacija seje
packets = []

# 1. Stranka pošlje zahtevek za sejo z nonce
client_nonce = os.urandom(4)
packets.append(IP(dst="100.100.100.100")/UDP(sport=54321, dport=12345)/Raw(load=b'\x02' + client_nonce))

# 2. Strežnik odgovori s ključem = sha256(nonce + secret)[:4]
key = generate_key(client_nonce)
packets.append(IP(src="100.100.100.100")/UDP(sport=12345, dport=54321)/Raw(load=b'\x02' + key))

# 3. Stranka pošlje zahtevek za seznam datotek
packets.append(IP(dst="100.100.100.100")/UDP(sport=54321, dport=12345)/Raw(load=b'\x00'))

# 4. Strežnik pošlje seznam z eno datoteko
file_list_response = b'\x03' + file_id + bytes([len(file_name)]) + file_name
packets.append(IP(src="100.100.100.100")/UDP(sport=12345, dport=54321)/Raw(load=file_list_response))

# 5. Stranka pošlje zahtevek za datoteko (offset = 0)
req = key + file_id + struct.pack("<I", 0)
packets.append(IP(dst="100.100.100.100")/UDP(sport=54321, dport=12345)/Raw(load=b'\x01' + req))

# 6. Strežnik pošlje šifriran del datoteke
encrypted_data = xor(flag, key)
packets.append(IP(src="100.100.100.100")/UDP(sport=12345, dport=54321)/Raw(load=b'\x01' + encrypted_data))

# 7. Zapiši v pcap
wrpcap("challenge.pcap", packets)
print(f"[+] PCAP zgeniran. Nonce: {client_nonce.hex()}, Key: {key.hex()}")
