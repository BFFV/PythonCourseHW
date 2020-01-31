# Aqui abajo debes escribir el código de tus clases
from abc import ABC, abstractmethod


class Ser(ABC):
    def __init__(self, name, atk, res, hp, ki):
        self.name = name
        self._hp = max(0, hp)
        self.atk = atk
        self.res = res
        self.ki = ki

    @property
    @abstractmethod
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    @abstractmethod
    def atacar(self, enemy):
        pass


class Humano(Ser):
    def __init__(self, *args, intelligence=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.int = intelligence

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    def meditar(self):
        self.ki += self.int/100
        print(f'Yo {self.name} estoy meditando!')

    def atacar(self, enemy):
        power = self.ki*(1 + self.atk - enemy.res)/2
        if power < 0:
            power = 0
        enemy.hp -= power
        print(f'{self.name} le quita {power} de vida a {enemy.name}')


class Extraterrestre(Ser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        else:
            self._hp = value

    def atacar(self, enemy):
        power = self.ki*(1 + self.atk - enemy.res)
        if power < 0:
            power = 0
        self.atk += self.atk*0.3
        enemy.hp -= power
        print(f'{self.name} le quita {power} de vida a {enemy.name}')


class Supersaiyayin(Extraterrestre, Humano):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def perder_cola(self):
        self.res -= self.res*0.6
        print(f'{self.name} perdió su cola!')


class Hakashi(Extraterrestre):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def robar_ki(self, *args):
        for e in args:
            steal = e.ki/2
            e.ki -= steal
            self.ki += steal


if __name__ == '__main__':
    """
    A continuación debes instanciar cada uno de los objetos pedidos,
    para que puedas simular la batalla.
    """
    h = Humano('Yamcha', 40, 40, 100, 100)
    s1 = Supersaiyayin('Goku', 1000, 1000, 10000, 2000, intelligence=10)
    s2 = Supersaiyayin('Vegeta', 800, 1000, 10000, 1800)
    h1 = Hakashi('Freezer', 700, 1000, 8000, 1500)
    h2 = Hakashi('Cell', 800, 1000, 10000, 2000)
    batalla = [h, s1, s2, h1, h2]
    for i in batalla:
        print(f'{i.name} atk: {i.atk} res: {i.res} vida: {i.hp} ki: {i.ki}\n')
    s1.atacar(h1)
    s1.atacar(h2)
    h1.robar_ki(s2,s1,h)
    for i in batalla:
        print(f'{i.name} atk: {i.atk} res: {i.res} vida: {i.hp} ki: {i.ki} \n')
    pass
