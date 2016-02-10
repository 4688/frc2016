#!/usr/bin/env python3

import socket as s

def startServer():

    TCP_IP = "10.46.88.2"
    TCP_PORT = 5800
    TCP_BUFF_SIZE = 2**5

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((TCP_IP, TCP_PORT))
    sock.listen(1)

    print("Listening for clients...")

    connection, address = sock.accept()
    print("Connected to client!")
    print("Connection address:", address[0] + "#" + str(address[1]))

    while True:
        data = connection.recv(TCP_BUFF_SIZE)
        if not data: break
        print("Received:", str(data.decode()))
        connection.send(data) # Echo

    connection.close()
