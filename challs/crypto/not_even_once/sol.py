from base64 import b64decode, b64encode
from pwn import *

p = remote("localhost", 1337)
p.recvuntil(b": ")
ct1 = p.recvline().strip()
print("ct1:", ct1)
ct1 = b64decode(ct1)

pt = b"A"*50
print("pt:", pt)
p.recvuntil(b"> ")
p.sendline(b"2")
p.sendline(pt)
ct2 = p.recvline().split(b": ")[-1].strip()
ct2 = b64decode(ct2)
print("ct2:", ct2)

# ct1 = flag ^ aes
# ct2 = pt ^ aes
# ct1 ^ flag = ct2 ^ pt
# flag = ct1 ^ ct2 ^ pt
flag = bytes([a ^ b ^ c for a, b, c in zip(ct1, ct2, pt)])
print("flag:", flag.decode().strip())
