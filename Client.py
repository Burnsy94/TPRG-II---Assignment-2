# TPRG II Assignment 2
# Alex Burns - 100885375

import socket

# Create a socket object, connect to the server
s = socket.socket()
host = '10.102.13.178'  # IP of Raspberry Pi, running the server
port = 5000

s.connect((host, port))

# Receive data from the server
data = s.recv(1024)  # Original buffer size

# Decode the bytes to a string
decoded_data = data.decode('utf-8')

# Print each line individually
for line in decoded_data.split('\\n'):
    print(line)

s.close()
