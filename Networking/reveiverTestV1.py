import socket
import numpy as np
import pickle

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 12345))
server_socket.listen(1)
print("Server is listening...")

# Accept a connection
client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

# Receive data
data = b""
while True:
    packet = client_socket.recv(4096)
    if not packet: break
    data += packet

# Deserialize the data
array = pickle.loads(data)
print("Received array:")
print(array)

client_socket.close()
server_socket.close()
