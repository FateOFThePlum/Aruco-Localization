import socket
import numpy as np
import pickle

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

# Create a NumPy array
array = np.array([[1, 2, 3], [4, 5, 6]])

# Serialize the array
data = pickle.dumps(array)

# Send data
client_socket.sendall(data)
client_socket.close()
