#!/usr/bin/env python3
import socket
import pickle

class tdClient:
    # client to send data to touchdesigner via tcp/ip

    # default_hostname = 'localhost'
    default_hostname = '10.0.0.4'
    default_port = 7000

    # initialize client. connects to given hostname and port upon init
    def __init__(self, hostname = default_hostname, port = default_port):
        self.hostname = hostname
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname, port))
        confirm_msg = self.s.recv(1024)
        print("confirmation: " + str(confirm_msg.decode("utf-8")))
        print("Client is connected to TouchDesigner!")

    # lazy method for sending data
    def sendData(self, data):
        data_encode = pickle.dumps(data)
        self.s.send(data_encode)
