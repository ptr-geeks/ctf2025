import random

with open("flag.txt", "r") as file:
    flag = file.read().strip()

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
def rand():
    return random.choice(alphabet)

rails_len = random.randint(2, 10)
random.seed(rails_len)
rails = []
for i, f in enumerate(flag):
    col = []
    for r in range(rails_len):
        # Rail fence cipher: place each character in a rail
        n = rails_len * 2 - 2
        pos = i % n
        if pos < n // 2:
            col.append(f if pos == r else rand())
        else:
            col.append(f if n - pos == r else rand())
    rails.append(col)

for j in range(rails_len):
    line = ""
    for i in range(len(rails)):
        line += rails[i][j]
    print(line)
