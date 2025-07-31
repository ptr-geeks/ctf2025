password = "ptr{if_you_can_read_this_you_are_once_again_cracked}"
password = [c for c in password]
prev = 0x41
for i in range(len(password)):
    password[i] = ord(password[i])
    password[i] = password[i] ^ prev
    password[i] = ~password[i]
    prev = password[i]
print(f"{len(password)} - {password}")
