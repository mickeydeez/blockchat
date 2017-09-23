#!/usr/bin/env python3

# lib/client.py

from lib.blockchain import Blockchain
import socket
import threading
import sys

class Client():
    
    def __init__(self, name, listener=True):
        host = socket.gethostname()
        port = 9998
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener = listener
        if listener:
            self.s.bind((host, port))
            self.s.listen(5)
        else:
            self.s.connect((host, port))
        self.clients = []
        self.blockchain = Blockchain(name)

    def run(self):
        if self.listener:
            client_socket, addr = self.s.accept()
            self.clients.append(client_socket)
        else:
            self.clients.append(self.s)
        send_thread = threading.Thread(
            name = 'send_thread',
            target = self.send_thread
        )
        recv_thread = threading.Thread(
            name = 'recv_thread',
            target = self.recv_thread
        )
        send_thread.start()
        recv_thread.start()
                
    def send_thread(self):
        try:
            while True:
                msg = input("%s> " % self.blockchain.id)
                if msg == "?chain":
                    print(self.blockchain.chain)
                else:
                    block = self.blockchain.send_block(msg)
                    for client in self.clients:
                        client.sendall(block.encode('utf-8'))
        except KeyboardInterrupt:
            sys.exit(1)

    def recv_thread(self):
        try:
            while True:
                if self.listener:
                    msg = self.clients[0].recv(1024)
                else:
                    msg = self.s.recv(1024)
                if msg:
                    block = self.blockchain.recv_block(msg.decode('utf-8'))
                    print(block['contents']['txns'])
        except KeyboardInterrupt:
            sys.exit(1)
