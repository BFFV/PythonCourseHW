import threading
import time
from itertools import chain
from random import randint, choices


def desencriptar(nombre_archivo):
    """
    Esta simple (pero útil) función te permite descifrar un archivo encriptado.
    Dado el path de un archivo, devuelve un string del contenido desencriptado.
    """

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        murcielago, numeros = "murcielago", "0123456789"
        dic = dict(chain(zip(murcielago, numeros), zip(numeros, murcielago)))
        return "".join(
            dic.get(char, char) for linea in archivo for char in linea.lower())


if __name__ == "__main__":
    class Equipo(threading.Thread):
        def __init__(self, nombre, lock, event):
            super().__init__()
            self.nombre = nombre
            self.hacker = Hacker(self.nombre)
            self.cracker = Cracker(self.nombre, lock)
            self.daemon = True
            self.event = event

        def run(self):
            self.hacker.start()
            self.cracker.start()
            self.hacker.join()
            self.cracker.join()
            print(f'El equipo {self.nombre} ha completado la misión!')
            self.event.set()


    class Hacker(threading.Thread):
        def __init__(self, equipo):
            super().__init__()
            self.equipo = equipo
            self.terminado = False
            self.daemon = True

        def run(self):
            print(f'El hacker del equipo {self.equipo} ha comenzado!')
            delay = randint(4, 12)
            time.sleep(delay)
            clave = desencriptar('pista.txt')
            print(f'El hacker del equipo {self.equipo} ha terminado '
                  f'la desencriptación: {clave}')
            self.terminado = True


    class Cracker(threading.Thread):
        def __init__(self, equipo, lock):
            super().__init__()
            self.equipo = equipo
            self.lineas = 0
            self.daemon = True
            self.lock = lock

        def run(self):
            print(f'El cracker del equipo {self.equipo} ha comenzado!')
            speed = randint(5, 15)
            if not (50 % speed):
                delay = 50 // speed
            else:
                delay = (50 // speed) + 1
            for minuto in range(delay):
                ataque = choices([True, False], [0.2, 0.8])
                if ataque:
                    with self.lock:
                        print(f'NebiLockbottom ha comenzado la '
                              f'reparación para el equipo {self.equipo}')
                        delay = randint(1, 3)
                        time.sleep(delay)
                        print(f'NebiLockbottom ha terminado '
                              f'la reparación para el equipo {self.equipo}')
                self.lineas += speed
                time.sleep(1)
            self.lineas = 50
            print(f'El cracker del equipo {self.equipo} ha terminado el código')

    class Mision:
        def __init__(self):
            self.equipos = []
            self.cracklock = threading.Lock()
            self.ganador = threading.Event()
            for i in range(3):
                self.equipos.append(
                    Equipo(str(i), self.cracklock, self.ganador))

        def run(self):
            for equipo in self.equipos:
                equipo.start()
            self.ganador.wait()
            for thread in self.equipos:
                if thread.hacker.terminado:
                    print(f'El hacker del equipo {thread.nombre} '
                          f'logró desencriptar el archivo!')
                else:
                    print(f'El hacker del equipo {thread.nombre} '
                          f'NO logró desencriptar el archivo!')
                print(f'El cracker del equipo {thread.nombre} '
                      f'escribió {thread.cracker.lineas} lineas!')
            for thread in self.equipos:
                if thread.cracker.lineas == 50:
                    print(f'El ganador es el equipo {thread.nombre}!!!')
    Mision().run()
