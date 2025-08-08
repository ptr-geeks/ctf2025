from scapy.all import IP, TCP, Raw, wrpcap
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

# Simulacija TCP seje
packets = []

# TCP handshake
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="S", seq=1000, ack=0))
packets.append(IP(src="203.0.113.15", dst="192.168.1.100")/TCP(sport=12345, dport=54321, flags="SA", seq=2000, ack=1001))
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="A", seq=1001, ack=2001))

# 1. Stranka pošlje zahtevek za sejo z nonce
client_nonce = os.urandom(4)
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="PA", seq=1001, ack=2001)/Raw(load=b'\x02' + client_nonce))

# 2. Strežnik odgovori s ključem = sha256(nonce + secret)[:4]
key = generate_key(client_nonce)
packets.append(IP(src="203.0.113.15", dst="192.168.1.100")/TCP(sport=12345, dport=54321, flags="PA", seq=2001, ack=1006)/Raw(load=b'\x02' + key))

# 3. Stranka pošlje zahtevek za seznam datotek
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="PA", seq=1006, ack=2006)/Raw(load=b'\x00'))

# 4. Strežnik pošlje seznam z eno datoteko
file_list_response = b'\x03' + file_id + bytes([len(file_name)]) + file_name
packets.append(IP(src="203.0.113.15", dst="192.168.1.100")/TCP(sport=12345, dport=54321, flags="PA", seq=2006, ack=1007)/Raw(load=file_list_response))

# 5. Stranka pošlje zahtevek za datoteko (offset = 0)
req = key + file_id + struct.pack("<I", 0)
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="PA", seq=1007, ack=2025)/Raw(load=b'\x01' + req))

# 6. Strežnik pošlje šifriran del datoteke
encrypted_data = xor(flag, key)
packets.append(IP(src="203.0.113.15", dst="192.168.1.100")/TCP(sport=12345, dport=54321, flags="PA", seq=2025, ack=1020)/Raw(load=b'\x01' + encrypted_data))

# TCP teardown
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="FA", seq=1020, ack=2041))
packets.append(IP(src="203.0.113.15", dst="192.168.1.100")/TCP(sport=12345, dport=54321, flags="FA", seq=2041, ack=1021))
packets.append(IP(src="192.168.1.100", dst="203.0.113.15")/TCP(sport=54321, dport=12345, flags="A", seq=1021, ack=2042))

# 7. Zapiši v pcap
wrpcap("challenge.pcap", packets)
print(f"[+] PCAP zgeniran. Nonce: {client_nonce.hex()}, Key: {key.hex()}")
