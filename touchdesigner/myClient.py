import socket
import pickle

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 7000))
# s.send("TEST\n".encode())
arr = ([0, 1, 2, 3, 4])
# data_string = pickle.dumps(arr)
# s.send('PLEASE\n'.encode())
s.send(bytes(2))
print('i tried :,)')

msg = s.recv(1024)
print(msg.decode("utf-8"))
# s.close()
