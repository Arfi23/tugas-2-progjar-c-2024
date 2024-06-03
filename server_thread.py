from socket import *
import socket
import threading
import logging
from time import gmtime, strftime

class RequestCommand:
    @staticmethod
    def time_cmd(connection):
        message = f"JAM {strftime('%H:%M:%S', gmtime())}\r\n"
        connection.sendall(message.encode("utf-8"))

    @staticmethod
    def quit_cmd(connection):
        message = "QUIT request diterima\r\n"
        connection.sendall(message.encode("utf-8"))
        connection.close()
    
    @staticmethod
    def unknown_cmd(connection):
        message = "WARNING: perintah tidak dikenali"
        connection.sendall(message.encode("utf-8"))

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
            while True:
                try:
                    data = self.connection.recv(1024)
                    if data:
                        command = data.decode('utf-8').strip()
                        logging.info(f"Data diterima: {command} dari client {self.address}.")
                        if command == 'TIME':
                            logging.info(f"Request berupa perintah TIME dari client {self.address}.")
                            RequestCommand.time_cmd(self.connection)
                        elif command == 'QUIT':
                            logging.info(f"Request berupa perintah QUIT dari client {self.address}.")
                            RequestCommand.quit_cmd(self.connection)
                            break
                        else:
                            logging.warning(f"Request {command} dari client {self.address} tidak dikenali.")
                            RequestCommand.unknown_cmd(self.connection)
                    else:
                        break
                except OSError:
                    break
            self.connection.close()

class Server(threading.Thread):
    def __init__(self, host='0.0.0.0', port=45000) :
        super().__init__()
        self.host = host
        self.port = port
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        self.my_socket.bind((self.host, self.port))
        self.my_socket.listen(1)
        logging.warning(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, cli_address = self.my_socket.accept()
            logging.warning(f"connection from {cli_address}")

            clt = ProcessTheClient(conn, cli_address)
            clt.start()
            self.the_clients.append(clt)


def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()