from pwn import *

forward = 5
iterations = 50
maxlen = 20
p = remote("localhost", 1337)

def recv(n):
    data = b""
    while len(data) < n:
        data += p.recv(n - len(data))
    return data

def recvbarrier():
    b = recv(8)
    f, t = u32(b[:4]), u32(b[4:])
    return f, t

def view(player, barriers):
    print("=" * maxlen)
    print("  Iteration: {}".format(i + 1))
    print("=" * maxlen)
    for f, t in barriers[::-1]:
        bar  = " " * f
        bar += "-" * (t - f + 1)
        print(bar)
    pl = "_" * player + "P" + "_" * (maxlen - player - 1)
    print(pl)


barriers = []
for _ in range(forward):
    barriers.append(recvbarrier())

player = 10

for i in range(iterations):
    view(player, barriers)

    moves = input("> ")
    moves = moves.lower().replace("a", "l").replace("d", "r").replace("s", "x")
    if len(moves) > 5:
        moves = moves[:5]
    if len(moves) <=5:
        moves += "x" * (5 - len(moves))
    for move in moves:
        if move == "l":
            player = max(0, player - 1)
        elif move == "r":
            player = min(maxlen - 1, player + 1)
        elif move != "x":
            print("Invalid move! Use 'a' for left, 'd' for right, and 's' for stay.")
    moves = moves.encode()

    p.send(moves)
    f, t = recvbarrier()
    barriers.append((f, t))
    barriers.pop(0)

p.interactive()
