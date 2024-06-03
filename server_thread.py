from socket import *
import socket
import threading
import logging
import time
import sys

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if data:
                self.connection.sendall(data)
            else:
                break
        self.connection.close()

