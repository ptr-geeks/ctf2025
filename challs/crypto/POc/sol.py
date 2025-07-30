from pwn import *
from paddingoracle import PaddingOracle, BadPaddingException
from base64 import b64encode, b64decode
from urllib.parse import quote, unquote

def unpack(data):
    data = data.strip()
    data = bytes.fromhex(data.decode())
    iv, ct = data[:16], data[16:]
    return ct, iv

def pack(ct, iv):
    data = iv + ct
    data = data.hex().encode()
    return data

p = remote('localhost', 1337)
ct, iv = unpack(p.recvline().split(b': ')[1])
print(f'IV: {iv.hex()}')
print(f'Ciphertext: {ct.hex()}')

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)

    def oracle(self, data, **kwargs):
        p.sendline(pack(data, iv))
        response = p.recvline().strip()
        if b'Invalid' in response:
            raise BadPaddingException

padbuster = PadBuster()
pt = padbuster.decrypt(ct, block_size=16, iv=iv)
print(f'Decrypted plaintext: {pt}')

p.interactive()
