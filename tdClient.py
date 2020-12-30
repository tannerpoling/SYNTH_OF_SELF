#!/usr/bin/env python3
import socket
import pickle

class tdClient:
    # client to send data to touchdesigner via tcp/ip

    # initialize client. connects to given hostname and port upon init
    def __init__(self, hostname = 'localhost', port = 7000):
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname, port))
        confirm_msg = self.s.recv(1024)
        print("confirmation: " + str(msg.decode("utf-8")))
        print("Client is connected to TouchDesigner!")

    # lazy method for sending data
    def sendData(data):
        data_encode = pickle.dumps(data)
        self.s.send(data_encode)
