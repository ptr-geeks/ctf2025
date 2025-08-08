import os
import socket
import struct
import threading
from dotenv import load_dotenv

load_dotenv()
FLAG = os.getenv("FLAG", "flag{dummy_flag}")

SESSION_KEY = b"\xab\xcd\xef\x01"
FILES = {
    b"\x00\x00\x00\x01": b"To tudi ni prava datoteka!",
    b"\x00\x00\x00\x02": FLAG.encode(),
    b"\x00\x00\x00\x03": b"Fake datoteka, ni flag.",
}

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def handle_client(conn, addr):
    print(f"Connected: {addr}")
    try:
        while True:
            data = conn.recv(2048)
            if not data:
                break
                
            cmd = data[0]
            if cmd == 0x02:
                # session key
                conn.send(b"\x02" + SESSION_KEY)
            elif cmd == 0x00:
                # file list
                response = b"\x03"
                for file_id, content in FILES.items():
                    name = f"file_{file_id.hex()}".encode()
                    response += file_id + bytes([len(name)]) + name
                conn.send(response)
            elif cmd == 0x01:
                body = data[1:]
                key = body[:4]
                file_id = body[4:8]
                offset = struct.unpack("<I", body[8:12])[0]
                content = FILES.get(file_id, b"")
                part = content[offset:offset+1024]
                encrypted = xor(part, key)
                conn.send(b"\x01" + encrypted)
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()
        print(f"Disconnected: {addr}")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("0.0.0.0", 12345))
sock.listen(5)
print("Server listening on port 12345...")

try:
    while True:
        conn, addr = sock.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()
except KeyboardInterrupt:
    print("\nShutting down server...")
finally:
    sock.close()
