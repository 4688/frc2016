#!/usr/bin/env python3

import socket as s

TCP_IP = "127.0.0.1"
TCP_PORT = 5800
TCP_BUFF_SIZE = 2**10

sock = s.socket(s.AF_INET, s.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send("Hello world from client!".encode())

data = sock.recv(TCP_BUFF_SIZE)
sock.close()

print("Received echo:", str(data.decode()))
