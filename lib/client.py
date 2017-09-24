#!/usr/bin/env python3

# lib/client.py

import socket, select, string, sys, base64
from lib.blockchain import Blockchain
import binascii
 
class Client(object):

    def __init__(self, name, host='127.0.0.1', port=5000):
        self.name = name
        self.blockchain = Blockchain(name)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((host, port))
        except:
            print("Unable to connect")
            sys.exit()
        print("Connected to the remote host")
        self.prompt()
        self.manage_responses()

    def prompt(self):
        sys.stdout.write('<%s> ' % self.name)
        sys.stdout.flush()
 
    def manage_responses(self):
        while True:
            socket_list = [sys.stdin, self.s]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
            for sock in read_sockets:
                if sock == self.s:
                    data = sock.recv(4096)
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        try:
                            decoded = base64.b64decode(data)
                            block = self.blockchain.recv_block(decoded)
                        except binascii.Error:
                            block = data.decode('utf-8')
                        sys.stdout.write(block)
                        self.prompt()
             
                else :
                    msg = sys.stdin.readline()
                    block = self.blockchain.send_block(msg)
                    payload = base64.b64encode(block.encode('utf-8'))
                    self.s.send(payload)
                    self.prompt()
