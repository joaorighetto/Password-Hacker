import string
import sys
import socket
from itertools import product

ip = sys.argv[1]
port = int(sys.argv[2])

char_base = list(string.ascii_lowercase + string.digits)

with socket.socket() as socket:
    socket.connect((ip, port))
    for i in range(1, 6):
        for item in list(product(char_base, repeat=i)):
            password = ''.join(item).encode()
            socket.send(password)
            response = socket.recv(64).decode()
            if response == "Connection success!":
                print(password.decode())
                break
        if response == "Connection success!":
            break
