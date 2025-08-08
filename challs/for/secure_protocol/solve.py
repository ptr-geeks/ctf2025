
import socket
import struct

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 12345))

# Get session key
sock.send(b"\x02")
key = sock.recv(5)[1:]
print("KEY:", key.hex())

# Get file list
sock.send(b"\x00")
file_list_data = sock.recv(1024)[1:]

files = {}
while file_list_data:
    fid = file_list_data[:4]
    name_len = file_list_data[4]
    name = file_list_data[5:5+name_len]
    files[fid] = name
    file_list_data = file_list_data[5+name_len:]

print("FILES:", {k.hex(): v for k, v in files.items()})

# Download each file
for fid in files:
    offset = 0
    data_total = b""
    while True:
        req = key + fid + struct.pack("<I", offset)
        sock.send(b"\x01" + req)
        response = sock.recv(2048)
        if response[0] != 0x01:
            break
        chunk = xor(response[1:], key)
        data_total += chunk
        if len(chunk) < 1024:
            break
        offset += len(chunk)
    print(f"FILE {files[fid].decode()}: {data_total.decode(errors='ignore')}")

sock.close()
