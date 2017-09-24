#!/usr/bin/env python3

# lib/server.py

import socket, select
 
class ChatServer(object):

    def __init__(self, host='0.0.0.0', port=5000):
        self.connection_list = []
        self.recv_buffer = 4096
        self.port = port
        self.host = host
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(10)
        self.connection_list.append(self.server_socket)
        print("Chat server started on port %s" % self.port)
        self.manage_connections()

    def manage_connections(self):
        while True:
        # Get the list sockets which are ready to be read through select
            read_sockets,write_sockets,error_sockets = select.select(self.connection_list,[],[])
    
            for sock in read_sockets:
                if sock == self.server_socket:
                    sockfd, addr = self.server_socket.accept()
                    self.connection_list.append(sockfd)
                    print("Client (%s, %s) connected" % addr)
                    self.broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
                else:
                    try:
                        data = sock.recv(self.recv_buffer).decode("utf-8")
                        if data:
                            self.broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data) 
                    except:
                        self.broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                        print("Client (%s, %s) is offline" % addr)
                        sock.close()
                        self.connection_list.remove(sock)
                        continue
     
        server_socket.close()

    def broadcast_data(self, sock, message):
        for socket in self.connection_list:
            if socket != self.server_socket and socket != sock :
                try :
                    socket.send(message.encode('utf-8'))
                except :
                    socket.close()
                    self.connection_list.remove(socket)
 
