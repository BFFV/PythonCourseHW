"""
client.py -- un simple cliente
"""

import pickle
from socket import socket, SHUT_RDWR

HOST = '127.0.0.1'


class Client:
    """
    Una clase que representa un cliente.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.socket = socket()
        self.connected = False

        # Este diccionario tiene los comandos disponibles.
        # Puedes modificarlo para agregar nuevos comandos.
        self.commands = {
            "help": self.help,
            "logout": self.logout,
            "ls": self.ls,
            "upload": self.upload,
            "download": self.download
        }

    def run(self):
        self.socket.connect((self.host, self.port))
        self.connected = True

        while self.connected:
            command, *args = input('$ ').split()
            function = self.commands.get(command)

            if function is None:
                print(f"El comando '{command}' no existe.")
                print("Escribe 'help' para obtener ayuda.")
            elif command == 'help':
                self.help()
            else:
                self.send(pickle.dumps((command, args)))
                function(*args)

    def send(self, message):
        msg_length = len(message).to_bytes(4, byteorder="big")
        self.socket.sendall(msg_length + message)

    def receive(self):
        byte_size = self.socket.recv(4)
        size = int.from_bytes(byte_size, byteorder="big")
        content = bytearray()
        while len(content) < size:
            content += self.socket.recv(min(4096, size - len(content)))
        return pickle.loads(content)

    def help(self):
        print("Esta es la lista de todos los comandos disponibles.")
        print('\n'.join(f"- {command}" for command in self.commands))

    def ls(self):
        file_list = self.receive()
        for file in file_list:
            print(file)

    def upload(self, *args):
        upload_list = list()
        for filename in args:
            with open(filename, 'rb') as file:
                upload_list.append(file.read())
        self.send(pickle.dumps(upload_list))

    def download(self, *args):
        index = 0
        names = list(args)
        new_files = pickle.loads(self.receive())
        for new_file in new_files:
            with open(names[index], 'wb') as file:
                file.write(new_file)
            index += 1

    def logout(self):
        self.connected = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        print("Arrivederci.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    client = Client(int(port_))
    client.run()
