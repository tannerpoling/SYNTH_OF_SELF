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


# import socket
# import pickle
# import threading
#
# def server_thread():
#     # address = 'localhost'
#     address = '10.0.0.4'
#     port = 7000
#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.bind((address, port))
#     s.listen(5)
#
#     print('test!')
#
#     while True:
#         clientsocket, address = s.accept()
#         print("Connection from: " + str(address))
#         # arr = (['synth1', 'synth2', 'synth3', 'synth4', 'synth5'], [0, 1, 2, 3, 4])
#         # test = dict(synth1=1, synth2=2, synth3=3)
#         # data_string = pickle.dumps(test)
#         msg = "success!"
#         # clientsocket.send(data_string)
#         clientsocket.send(bytes(msg, "utf-8"))
#         while True:
#             data = clientsocket.recv(4096)
#             try:
#                 data_decode = pickle.loads(data)
#                 print(str(data_decode))
#             except EOFError:
#                 clientsocket.close()
#
# if __name__ == "__main__":
#     mainthread = threading.Thread(target=server_thread, args=())
#     mainthread.start()
