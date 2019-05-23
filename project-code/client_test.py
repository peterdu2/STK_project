import socket
import sys



s = socket.socket()
port = 8080
s.connect(('127.0.0.1', port))

while True:
# connect to the server on local computer
    features = s.recv(1024)
    print(features.decode())
