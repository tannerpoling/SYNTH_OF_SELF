import socket
import pickle
import threading
import numpy as np
import queue

debug = False

def server_thread():
    # address = 'localhost'
    address = '10.0.0.4'
    port = 7000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((address, port))
    s.listen(5)

    print('server start!')

    while True:
        clientsocket, address = s.accept()
        print("Connection from: " + str(address))
        # arr = (['synth1', 'synth2', 'synth3', 'synth4', 'synth5'], [0, 1, 2, 3, 4])
        # test = dict(synth1=1, synth2=2, synth3=3)
        # data_string = pickle.dumps(test)
        msg = "successful conncection!"
        # clientsocket.send(data_string)
        clientsocket.send(bytes(msg, "utf-8"))
	# now recieve data from client
        while True:
            data = clientsocket.recv(4096)
            try:
                data_decode = pickle.loads(data)
                if debug:
                	print(str(data_decode))
                	print('synth1: ' + str(data_decode[:,0]))
                myInQ.put(data_decode)
                # for i in range(data_decode.shape[0]):
                #     for j in range(data_decode.shape[1]):
                #         n[i+1, j+1] = data_decode[i][j]

            except EOFError:
                clientsocket.close()

n = op('synthtable')
n.setSize(5, 5)
n.replaceRow(0, [None, 'synth0', 'synth1', 'synth2', 'synth3'])
n.replaceCol(0, [None, 'freq', 'gain', 'mod', 'enable'])

myInQ = queue.Queue()
me.parent().store('inQ', myInQ)
me.parent().storeStartupValue('inQ', None) 


mainthread = threading.Thread(target=server_thread, args=())
mainthread.start()
