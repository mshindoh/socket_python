'''
Reference: https://realpython.com/courses/python-sockets-part-1/
'''

#!/usr/bin/env python3

'''
In terminal,
python echo-server.py
In another terminal session,
python echo-client.py
'''

# echo-server.py

import socket 

# 1 - Server sets up a listening socket

HOST = "127.0.0.1"

PORT = 65432

# create listening scocket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # bind the socket to HOST and PORT to listen to
    s.listen() # listen for request
    conn, addr = s.accept() # wait to accept connection
    # conn - new socket to send/receive data
    # addr - internet address of the client

# 3 - Data is exchanged

    with conn: # open new socket
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024) # read up to 1KB of data
            if not data:
                break
            conn.sendall(data)

