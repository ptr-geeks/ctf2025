import random

with open("flag.txt", "r") as f:
    flag = f.read().strip()

def cesar_cipher(text, shift):
    result = []
    for char in text:
        if ord(char) >= ord('a') and ord(char) <= ord('z'):
            shifted = (ord(char) - ord('a') + shift) % 26 + ord('a')
            result.append(chr(shifted))
        else:
            result.append(char)
    return ''.join(result)

shift = random.randint(1, 25)
ciphertext = cesar_cipher(flag, shift)
print(ciphertext)
