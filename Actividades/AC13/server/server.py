"""
server.py -- un simple servidor
"""

import pickle
from socket import socket
from os import listdir, getcwd

HOST = '127.0.0.1'


class Server:
    """
    Una clase que representa un servidor.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.client = None
        self.socket = socket()

        self.commands = {
            "ls": self.list_filenames,
            "download": self.send_file,
            "upload": self.save_file,
            "logout": self.disconnect,
        }

    def run(self):
        """
        Enciende el servidor que puede conectarse
        y recibir comandos desde un único cliente.
        """

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Escuchando en {self.host}:{self.port}.")

        while self.client is None:
            self.client, _ = self.socket.accept()
            print("¡Un cliente se ha conectado!")

            while self.client:
                command, args = pickle.loads(self.receive())
                self.commands[command](*args)

        print("Arrivederci.")

    def send(self, message):
        pickle_msg = pickle.dumps(message)
        msg_length = len(pickle_msg).to_bytes(4, byteorder="big")
        self.client.sendall(msg_length + pickle_msg)

    def receive(self):
        byte_size = self.client.recv(4)
        size = int.from_bytes(byte_size, byteorder="big")
        content = bytearray()
        while len(content) < size:
            content += self.client.recv(min(4096, size - len(content)))
        return content

    def list_filenames(self):
        self.send(listdir(getcwd()))

    def send_file(self, *args):
        upload_list = list()
        for filename in args:
            with open(filename, 'rb') as file:
                upload_list.append(file.read())
        self.send(pickle.dumps(upload_list))

    def save_file(self, *args):
        index = 0
        names = list(args)
        new_files = pickle.loads(self.receive())
        for new_file in new_files:
            with open(names[index], 'wb') as file:
                file.write(new_file)
            index += 1

    def disconnect(self):
        self.client = None
        print("El cliente se ha desconectado.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    server = Server(int(port_))
    server.run()
