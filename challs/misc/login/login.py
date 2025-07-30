import socket
import threading
import random
import os

MAX_ATTEMPTS = 3
SECRET = os.getenv("FLAG")
if not SECRET:
    print("Please set the FLAG environment variable.")
    exit(1)

class Database:
    def __init__(self):
        self.users = {}

    def insert(self, username, pin):
        self.users[username] = {"pin": pin, "pin_attempts": 0}

    def get(self, username):
        return self.users.get(username)

    def set(self, username, user_data):
        self.users[username] = user_data

db = Database()

def recvline(client):
    line = b""
    while True:
        char = client.recv(1) # Read one byte at a time
        if not char or char == b'\n':
            break # Return on empty or newline
        line += char
    return line.decode('utf-8')

def handle_client(client):
    client.send(b"Username: ")
    username = recvline(client)
    user = db.get(username)
    if not user:
        client.close()
        return # User not found
    if user["pin_attempts"] >= MAX_ATTEMPTS:
        client.close()
        return # Too many attempts
    client.send(b"PIN: ")

    pin = recvline(client)
    if pin != user["pin"]:
        user["pin_attempts"] += 1 # Increase and save pin attempts
        db.set(username, user)
        client.close()
        return # Incorrect PIN

    client.send(b"Admin only secret: " + SECRET.encode('utf-8') + b"\n")
    client.close()


# Set random 4 digit pin for admin user
randpin = str(random.randint(0, 9999)).rjust(4, '0')
db.insert("admin", randpin)
print(f"Admin user created with PIN: {randpin}")
# Open socket and listen for connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 1337))
server.listen(12345)
# Handle connections (in separate threads for max performance!!!)
while True:
    client_socket, addr = server.accept()
    threading.Thread(target=handle_client, args=(client_socket,)).start()

