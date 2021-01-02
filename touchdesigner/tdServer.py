import socket
import pickle

# address = 'localhost'
address = '10.0.0.4'
port = 7000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((address, port))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print("Connection from: " + str(address))
    # arr = (['synth1', 'synth2', 'synth3', 'synth4', 'synth5'], [0, 1, 2, 3, 4])
    # test = dict(synth1=1, synth2=2, synth3=3)
    # data_string = pickle.dumps(test)
    msg = "success!"
    # clientsocket.send(data_string)
    clientsocket.send(bytes(msg, "utf-8"))
    while True:
        data = clientsocket.recv(4096)
        try:
            data_decode = pickle.loads(data)
            print(str(data_decode))
        except EOFError:
            clientsocket.close()
