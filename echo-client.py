'''
Reference: https://realpython.com/courses/python-sockets-part-1/
'''

#!/usr/bin/env python3

# 2 - Client initiates a connection

import socket 

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # connect the socket to HOST and PORT

# 3 - Data is exchanged 

    s.sendall(b"Hello, world") # send in 8 bit unit
    data = s.recv(1024)

print(f"Received {data}")
