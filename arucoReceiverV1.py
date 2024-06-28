import cv2
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
while True: 
    try:
        # Receive data
        data = b""
        while True:
            packet = client_socket.recv(500000)
            if not packet: break
            data += packet
            print(len(data))
            
            if len(data)>231:break
        #if input(len(data)) == "GO": break

        print("Received...")

        # Deserialize the data
        array = pickle.loads(data)
        #cv2.imshow("Frame", array[0][0])
        #cv2.waitKey(1)
        print("Received array:")
        print(array)
    except:
        print("error")
        data = b""
client_socket.close()
server_socket.close()
