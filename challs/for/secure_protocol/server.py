import os
import socket
import struct
from dotenv import load_dotenv

load_dotenv()
FLAG = os.getenv("FLAG", "flag{dummy_flag}")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 12345))

SESSION_KEY = b"\xab\xcd\xef\x01"
FILES = {
    b"\x00\x00\x00\x01": b"To tudi ni prava datoteka!",
    b"\x00\x00\x00\x02": FLAG.encode(),
    b"\x00\x00\x00\x03": b"Fake datoteka, ni flag.",
}

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

while True:
    data, addr = sock.recvfrom(2048)
    if not data:
        continue
    cmd = data[0]
    if cmd == 0x02:
        # session key
        sock.sendto(b"\x02" + SESSION_KEY, addr)
    elif cmd == 0x00:
        # file list
        response = b"\x03"
        for file_id, content in FILES.items():
            name = f"file_{file_id.hex()}".encode()
            response += file_id + bytes([len(name)]) + name
        sock.sendto(response, addr)
    elif cmd == 0x01:
        body = data[1:]
        key = body[:4]
        file_id = body[4:8]
        offset = struct.unpack("<I", body[8:12])[0]
        content = FILES.get(file_id, b"")
        part = content[offset:offset+1024]
        encrypted = xor(part, key)
        sock.sendto(b"\x01" + encrypted, addr)
