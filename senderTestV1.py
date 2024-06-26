import socket
import numpy as np

# Server IP address and port
HOST = "localhost"
PORT = 5000

# Create two NumPy arrays
arr1 = np.array([1, 2, 3])
arr2 = np.array([[4, 5], [6, 7]])

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
sock.connect((HOST, PORT))

# Send the shape and data of each array
for arr in [arr1, arr2]:
    # Send the shape of the array
    sock.sendall(str(arr.shape).encode())
    # Send the data of the array as bytes
    sock.sendall(arr.tobytes())

print("Sent arrays to server")

# Close the socket
sock.close()
