import socket
import pickle

# address = 'localhost'
address = '10.0.0.4'
port = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
# s.send("TEST\n".encode())
# arr = ([0, 1, 2, 3, 4])
# data_string = pickle.dumps(arr)
# s.send(arr)
# s.send('PLEASE\n'.encode())
# s.send(bytes(2))
# print('i tried :,)')

msg = s.recv(4096)
msg_decode = pickle.loads(msg)
print("recieved message: ")
print(str(msg_decode))
# s.close()
