from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os
from base64 import b64encode, b64decode

changed = False
key = os.urandom(16)
iv = os.urandom(8)
with open('flag.txt', 'r') as f:
    flag = f.read().strip().encode()

def enc(data, key, iv):
    data = pad(data, AES.block_size)
    aes = AES.new(key, AES.MODE_CTR, nonce=iv)
    return aes.encrypt(data)

def dec(data, key, iv):
    aes = AES.new(key, AES.MODE_CTR, nonce=iv)
    data = aes.decrypt(data)
    return unpad(data, AES.block_size)

def menu():
    print("1. Change key and IV")
    print("2. Encrypt message")
    print("3. Decrypt message")
    print("4. Exit")
    return input("> ").strip()

def menu_change():
    global key
    global iv
    global changed

    new_key = input("Enter new key in base64: ").strip()
    new_iv = input("Enter new IV in base64: ").strip()

    try:
        key = b64decode(new_key)
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes long.")

        iv = b64decode(new_iv)
        if len(iv) != 8:
            raise ValueError("IV must be 8 bytes long.")

        changed = True
    except Exception as e:
        print(f"Error changing key: {e}")

def menu_encrypt():
    message = input("Enter message to encrypt: ").strip().encode()
    try:
        encrypted_message = enc(message, key, iv)
        print("Encrypted message in base64:", b64encode(encrypted_message).decode())
    except Exception as e:
        print(f"Error encrypting message: {e}")

def menu_decrypt():
    if not changed:
        print("I'm not letting you use my config! Change it first!")
        return

    message = input("Enter message to decrypt in base64: ").strip()
    try:
        message = b64decode(message)
        decrypted_message = dec(message, key, iv)
        print("Decrypted message:", decrypted_message.decode())
    except Exception as e:
        print(f"Error decrypting message: {e}")

encflag = enc(flag, key, iv)
encflag = b64encode(encflag).decode()
print("Look at my magic encryption machine!")
print("Let me show you, here's my encrypted flag in base64:", encflag)
print("Here, try it out!")

while True:
    choice = menu()
    if choice == '1':
        menu_change()
    elif choice == '2':
        menu_encrypt()
    elif choice == '3':
        menu_decrypt()
    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid choice, please try again.")
