import socket
import sys

s = socket.socket()
print("Socket successfully created")
port = 6969

s.bind(('', port))
print("socket binded to %s" %(port))

s.listen(5)
print("socket is listening")

while True:

   # Establish connection with client.
   c, addr = s.accept()
   print('Got connection from', addr)

   # send a thank you message to the client.
   #c.send("Thank you for connecting")
   #message='test'
   #c.sendto(message.encode(),("127.0.0.1", 50050))

   # Close the connection with the client
   c.close()
