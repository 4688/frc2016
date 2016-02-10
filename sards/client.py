#!/usr/bin/env python3

import socket as s

def connect():

    TCP_IP = "10.46.88.2"
    TCP_PORT = 5800
    TCP_BUFF_SIZE = 2**10

    print("Starting client...")

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    print("init socket")
    sock.connect((TCP_IP, TCP_PORT))
    print("connected")
    sock.send("Hello world from client!".encode())
    print("sent")

    data = sock.recv(TCP_BUFF_SIZE)
    print("received")
    sock.close()

    print("Received echo:", str(data.decode()))
