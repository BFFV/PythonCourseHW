class Terreno:
    def __init__(self, nombre):
        self.nombre = nombre


class Ciudad:
    def __init__(self, path):
        self.city = dict()
        with open(path, encoding='utf-8') as file:
            for line in file:
                origen, destinos = line.strip().split(':')
                for nodo in destinos[1:].split(','):
                    self.agregar_calle(Terreno(origen).nombre,
                                       Terreno(nodo).nombre)

    def agregar_calle(self, origen, destino):
        if origen not in self.city:
            self.city[origen] = set()
        if destino not in self.city:
            self.city[destino] = set()
        self.city[origen].add(destino)

    def eliminar_calle(self, origen, destino):
        if (origen or destino) not in self.city:
            return ()
        if destino not in self.city[origen]:
            return ()
        self.city[origen].remove(destino)
        return origen, destino

    @property
    def terrenos(self):
        return {t for t in self.city}

    @property
    def calles(self):
        return {(c, dest) for c in self.city for dest in self.city[c]}

    def verificar_ruta(self, ruta):
        if not len(ruta):
            return True
        if len(ruta) == 1:
            return ruta[0] in self.city
        for i in range(len(ruta) - 1):
            if ruta[i + 1] not in self.city.get(ruta[i], None):
                return False
        return True

    def entregar_ruta(self, origen, destino):
        if (origen or destino) not in self.city:
            return []
        if origen == destino:
            return [origen]
        visitados = set()
        queue = [[origen]]
        while queue:
            camino = queue.pop(0)
            actual = camino[-1]
            if actual not in visitados:
                vecinos = [x for x in self.city[actual]]
                for v in vecinos:
                    queue.append(list(camino + [v]))
                    if v == destino:
                        return queue[-1]
                visitados.add(actual)
        return []

    def ruta_corta(self, origen, destino):
        return self.entregar_ruta(origen, destino)

    def ruta_entre_bombas(self, origen, *destinos):
        if origen not in self.city:
            return []
        for dest in destinos:
            if dest not in self.city:
                return []
        if origen == destinos[-1]:
            return [origen]
        dest = tuple(destinos)
        visitados = set()
        queue = [[origen]]
        while queue:
            camino = queue.pop(0)
            actual = camino[-1]
            if actual not in visitados:
                vecinos = [x for x in self.city[actual]]
                for v in vecinos:
                    queue.append(list(camino + [v]))
                    if v == destinos[-1]:
                        d_list = list(dest)
                        bombs = 0
                        for i in range(len(queue[-1])):
                            if queue[-1][i] == d_list[bombs]:
                                bombs += 1
                        if bombs == len(destinos):
                            return queue[-1]
                visitados.add(actual)
        return []

    def ruta_corta_entre_bombas(self, origen, *destinos):
        return self.ruta_entre_bombas(origen, *destinos)


if __name__ == '__main__':
    f = Ciudad('facil.txt')
    m = Ciudad('medio.txt')
    d = Ciudad('dificil.txt')
    k = Ciudad('kratos.txt')
    print(f.ruta_entre_bombas('A', 'E', 'F'))
    print(m.ruta_entre_bombas('A', 'E', 'F'))
    print(d.ruta_entre_bombas('A', 'E', 'F'))
    print(k.ruta_entre_bombas('A', 'E', 'F'))
