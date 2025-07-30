from Crypto.Cipher import AES
import os

key = os.urandom(16)
iv = os.urandom(16)
with open('flag.txt', 'r') as f:
    flag = f.read().strip().encode()

def pad(data, bs=16):
    l = (bs - len(data) % bs)
    return data + bytes([l] * l)

def valid(data):
    l = data[-1]
    if l < 1 or l > 16:
        return False
    return data[-l:] == bytes([l] * l)

def unpad(data):
    l = data[-1]
    return data[:-l]

def enc(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = pad(data)
    return cipher.encrypt(data)

def dec(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = cipher.decrypt(data)
    return data

flag_enc = iv + enc(flag, key, iv)
print(f'Encrypted flag: {flag_enc.hex()}')

while True:
    ct = input('Enter ciphertext to decrypt (hex): ')
    ct = bytes.fromhex(ct.strip())
    iv, ct = ct[:16], ct[16:]
    pt = dec(ct, key, iv)
    if not valid(pt):
        print('Invalid')
        continue
    pt = unpad(pt)
    print(len(pt), 'bytes decrypted')
