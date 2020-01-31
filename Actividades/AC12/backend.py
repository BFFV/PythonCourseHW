import json
import os
import os.path as path
import pickle

from clases import Comida, ComidaEncoder

BOOK_PATH = 'recetas.book'


class PyKitchen:
    def __init__(self):
        self.recetas = []
        self.comidas = []
        self.despachadas = []

    def cargar_recetas(self):
        with open('recetas.book', 'rb') as file:
            recipes = pickle.load(file)
            for recipe in recipes:
                self.recetas.append(recipe)


    def guardar_recetas(self):
        with open('recetas.book', 'wb') as file:
            pickle.dump(self.recetas, file)


    def cocinar(self):
        verified = [x for x in self.recetas if x.verificada]
        food = [Comida.de_receta(x) for x in verified]
        for f in food:
            with open(f'horno/{f.nombre}.json', 'w') as file:
                json.dump(f, file, cls=ComidaEncoder)

    def despachar_y_botar(self):
        foods = [x for x in os.listdir('horno') if x.endswith('.json')]
        for f in foods:
            with open(os.path.join(os.getcwd() + "/horno", f)) as file:
                loaded = json.load(file)
                plate = Comida(*[loaded[x] for x in loaded])
                if not plate.preparado:
                    self.comidas.append(plate)
                elif plate.preparado and not plate.quemado:
                    self.despachadas.append(plate)
                else:
                    print(f'{plate.nombre} se quemó!!! ')
