#!/usr/bin/env python3

# lib/client

from lib.blockchain import Blockchain
import socket
import threading
import sys

class Client(threading.Thread):

    def __init__(self, conn, name='foo'):
        super(Client, self).__init__()
        self.conn = conn
        self.chain = Blockchain(name)

    def run(self):
        while True:
            buf = self.conn.recv(1024)
            self.chain.recv_block(buf.decode('utf-8'))

    def send_msg(self,msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()

class Connection(threading.Thread):

    def __init__(self, host, port, listener=True):
        super(Connection, self).__init__()
        self.listener = listener
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if listener:
                self.s.bind((host,port))
                self.s.listen(5)
            else:
                self.s.connect((host,port))
        except socket.error:
            print('Failed to create socket')
            sys.exit()
        self.clients = []

    def run(self):
        while True:
            if self.listener:
                conn, address = self.s.accept()
                c = Client(conn)
                c.start()
                c.send_msg("\r\n".encode('utf-8'))
                self.clients.append(c)
                print('[+] Client connected: {0}'.format(address[0]))
            else:
                try:
                    response = input() 
                    for c in self.clients:
                        message = "%s\n" % response
                        msg = message.encode('utf-8')
                        c.send_msg(msg)
                except KeyboardInterrupt:
                    sys.exit()

