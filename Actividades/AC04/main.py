class Aventurero:
    def __init__(self, name, attack, speed):
        self.name = name
        self._hp = 100
        self.attack = attack
        self.speed = speed

    @property
    def power(self):
        return self._hp + self.attack + self.speed

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, n):
        if n > 100:
            self._hp = 100
        elif n < 0:
            self._hp = 0
        else:
            self._hp = n

    def grito_de_guerra(self):
        print("Nombre: " + self.name + "\n¡Gloria al gran Tini!")


class Guerrero(Aventurero):
    def __init__(self, name, attack, speed, defense):
        super().__init__(name, attack, speed)
        self.defense = defense

    @property
    def power(self):
        return 0.8*self._hp + 2.2*self.attack + 1.5*self.defense \
               + 0.5*self.speed


class Mago(Aventurero):
    def __init__(self, name, attack, speed, magic):
        super().__init__(name, attack, speed)
        self.magic = magic

    @property
    def power(self):
        return self._hp + 0.1*self.attack + 2.5*self.magic + 1.4*self.speed


class Monstruo:
    def __init__(self, name, hp, power, boss):
        self.name = name
        self._hp = hp
        self.power = power
        if boss:
            self.power *= 3

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, n):
        if n < 0:
            self._hp = 0
        else:
            self._hp = n


class Clan:
    def __init__(self, name, members):
        self.name = name
        if members == "":
            self.members = []
        else:
            self.members = members

    @property
    def rank(self):
        if len(self.members) < 3:
            return "Bronce"
        elif 2 < len(self.members) < 6:
            return "Plata"
        else:
            return "Oro"

    @property
    def power(self):
        total = 0
        if self.rank == "Bronce":
            a = 0.5
        elif self.rank == "Plata":
            a = 0.75
        else:
            a = 1.2
        for i in self.members:
            total += i.power*a
        return total

    def agregar(self, adventurer):
        if isinstance(adventurer, Aventurero):
            self.members.append(adventurer)
        else:
            print("No es posible agregar monstruos a los clanes")

    def remover(self, adventurer):
        if adventurer in self.members:
            self.members.pop(self.members.index(adventurer))
        else:
            print("Entidad no encontrada")

    def __add__(self, other):
        if isinstance(other, Clan):
            return Clan(self.name + other.name, self.members + other.members)
        else:
            print("No se pueden mezclar clanes con mazmorras")


class Mazmorra:
    def __init__(self, name, monsters):
        self.name = name
        if monsters == "":
            self.monsters = []
        else:
            self.monsters = monsters

    @property
    def power(self):
        total = 0
        for i in self.monsters:
            total += i.power
        return total

    def agregar(self, monster):
        if isinstance(monster, Monstruo):
            self.monsters.append(monster)
        else:
            print("No es posible agregar personas a las mazmorras")

    def remover(self, monster):
        if monster in self.monsters:
            self.monsters.pop(self.monsters.index(monster))
        else:
            print("Entidad no encontrada")

    def __add__(self, other):
        if isinstance(other, Mazmorra):
            return Mazmorra(self.name + other.name, self.monsters
                            + other.monsters)
        else:
            print("No se pueden mezclar clanes con mazmorras")
