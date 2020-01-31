from collections import defaultdict

class Nodo:
    def __init__(self, rango, items):
        self.rango = rango
        self.items = items
        self.superior = None
        self.superiores = None
        self.subordinados = defaultdict(Nodo)


class Ejercito:
    def __init__(self, general):
        self.general = general
        self.rangos = ['General', 'Teniente', 'Mayor', 'Capitán', 'Soldado']


    def agregar_subordinado(self, entidad):
        if not self.root:
            self.root = entidad
        else:
            if not self.root.subs:
                self.root.subordinados[entidad] = entidad.subordinados
            else:
                index = self.rangos.index(entidad.rango)
                sup = self.rangos[:index - 1]
                for subs in self.root.subordinados:
                    pass
                if self.root.rango in sup:
                    pass
                else:
                    pass


def cargar(ejercito):
    army = Arbol()
    with open(f'{ejercito}.csv', encoding='utf-8') as file:
        for data in file:
            entidad = data.strip().split(',')
            army.agregar_subordinado(Nodo(entidad[0], set(entidad[1:])))
    return army

ejercito = cargar('ejercito_1')
print(ejercito.root.items)
