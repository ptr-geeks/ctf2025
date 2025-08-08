from scapy.all import rdpcap, TCP, Raw, IP
import struct

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Naloži pcap datoteko
packets = rdpcap("challenge.pcap")

key = None
files = {}
file_data = {}
requests = {}

# 1. Najdi ključ (odgovor na 0x02)
for pkt in packets:
    if TCP in pkt and Raw in pkt:
        data = pkt[Raw].load
        if data.startswith(b"\x02") and len(data) == 5 and pkt[IP].src == "203.0.113.15" and pkt[TCP].sport == 12345:
            key = data[1:]
            print(f"[+] Key found: {key.hex()}")
            break

if key is None:
    print("[-] Key not found.")
    exit()

# 2. Najdi seznam datotek (0x03)
for pkt in packets:
    if TCP in pkt and Raw in pkt:
        data = pkt[Raw].load
        if data.startswith(b"\x03") and pkt[IP].src == "203.0.113.15" and pkt[TCP].sport == 12345:
            payload = data[1:]
            while payload:
                fid = payload[:4]
                name_len = payload[4]
                name = payload[5:5 + name_len]
                files[fid] = name.decode()
                payload = payload[5 + name_len:]

print(f"[+] Files: {[v for v in files.values()]}")

# 3. Shrani vse zahteve za datoteke (0x01 request)
for pkt in packets:
    if TCP in pkt and Raw in pkt:
        data = pkt[Raw].load
        if data.startswith(b"\x01") and pkt[TCP].dport == 12345:
            raw = data[1:]
            if len(raw) >= 12:
                fid = raw[4:8]
                offset = struct.unpack("<I", raw[8:12])[0]
                requests[offset] = fid

# 4. Zberi odgovore (0x01 response) in dešifriraj
for pkt in packets:
    if TCP in pkt and Raw in pkt:
        data = pkt[Raw].load
        if data.startswith(b"\x01") and pkt[IP].src == "203.0.113.15" and pkt[TCP].sport == 12345:
            encrypted = data[1:]
            decrypted = xor(encrypted, key)

            # heuristika: offseti pridejo v enakem vrstnem redu
            offset = len(file_data) * 1024
            fid = requests.get(offset, next(iter(files)))

            if fid not in file_data:
                file_data[fid] = b""
            file_data[fid] += decrypted

# 5. Izpiši vsebino datotek
for fid, content in file_data.items():
    name = files.get(fid, fid.hex())
    print(f"\n--- FILE {name} ---")
    print(content.decode(errors="ignore"))
