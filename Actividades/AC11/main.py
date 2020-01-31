import os


def buscar_archivo(nombre, cwd=os.getcwd()):
    for root, dir, files in os.walk(cwd):
        if nombre in files:
            return root + f'/{nombre}'


def leer_archivo(path):
    with open(path, 'rb') as file:
        binary = []
        final = []
        for byte in bytearray(file.read()):
            transform = bin(byte)[2:]
            while len(transform) < 7:
                transform = '0' + transform
            binary.append(transform)
        for n in range(len(binary) - 1):
            word = (binary[n] + binary[n + 1]).lstrip('0')
            if word:
                final.append(word[1:])
        return final





def decodificar(bits):
    indexes = []
    n = 0
    while ((2 ** n) - 1) < len(bits):
        indexes.append((2 ** n) - 1)
        n += 1
    print(indexes)
    for index in indexes:
        n = index
        skip = index + 1
        while n < len(bits):
            pass
            n += index




def escribir_archivo(ruta, chunks):
    pass


# Aquí puedes crear todas las funciones extra que requieras.


if __name__ == "__main__":
    nombre_archivo_de_pista = "himno.shrek"
    ruta_archivo_de_pista = buscar_archivo(nombre_archivo_de_pista)

    chunks_corruptos_himno = leer_archivo(ruta_archivo_de_pista)

    chunks_himno = [decodificar(chunk) for chunk in chunks_corruptos_himno]

    nombre_ubicacion_himno = "himno.png"
    escribir_archivo(nombre_ubicacion_himno, chunks_himno)
