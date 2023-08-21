'''
Reference: https://realpython.com/courses/python-sockets-part-1/
'''

#!/usr/bin/env python3

'''
In a terminal, python multiconn-server.py 127.0.0.1 65432
In another terminal session, python multiconn-client.py 127.0.0.1 65432 3
'''

# multiconn-server.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

# last part of Phase 1
def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"") # simple object with custom attributes
    events = selectors.EVENT_READ | selectors.EVENT_WRITE # create event mask (socket with both read and write)
    sel.register(conn, events, data=data) # register the socket to the selector


# 3 - Data is exchanged

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        # read from the socket
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            # append the data to the output
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            # un-register it from the selector
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb: # there should always be data
            print(f"Echoing {data.outb} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write, send the data and returns bytes sent
            data.outb = data.outb[sent:] # strip off the bytes sent from the output data


####

# diagnostic check
# if there are no 3 arguments, the program exits while displaying the reason
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

# 1 - Server sets up a listening socket

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")
lsock.setblocking(False) # do not block the socket
sel.register(lsock, selectors.EVENT_READ, data=None) # register socket to selector

# event loop
try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            # key: information about the data into the socket
            # mask: type of event
            if key.data is None: # listening socket
                accept_wrapper(key.fileobj) # to end Phase 1
            else: # processing communication
                service_connection(key, mask) # to start Phase 3
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()
