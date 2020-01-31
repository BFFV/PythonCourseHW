from gui.entities import Human, Game, Building
import random as r
import names as n
import math as m
import parameters as par


class Client(Human):
    _id = 0

    def __init__(self, personality, x=0, y=0):
        super().__init__(personality, x, y)
        self.id = Client._id
        Client._id += 1
        self.name = n.get_full_name()
        self.age = r.randint(18, 80)
        self.personality = personality
        self.active = True
        self.social = False
        attributes = get_attributes(personality)
        self.wealth = attributes[0]
        self.sociability = attributes[1]
        self._anxiety = attributes[2]
        self._lucidity = attributes[3]
        self._luck = attributes[4]
        self._stamina = attributes[5]
        self._dishonesty = attributes[6]
        self._money = 200 * self.wealth
        self.gangster = False
        self.busy = False
        self.walking = False
        self.next_location = None
        self.aux_location = None
        self.wait_time = 0
        self.waiting = False
        self.predict_rounds = 0
        self.cheat = False
        self.expelled = False
        self.next = None
        self.time = 0

    @property
    def anxiety(self):
        boost = 1
        if (self._money > 400 * self.wealth) or (self._money < 40 *
                                                 self.wealth):
            boost = 1.25
        return min(1, self._anxiety * boost)

    @anxiety.setter
    def anxiety(self, value):
        self._anxiety = round(max(0, min(value, 1)), 3)

    @property
    def lucidity(self):
        return self._lucidity

    @lucidity.setter
    def lucidity(self, value):
        self._lucidity = round(max(0, min(value, 1)), 3)

    @property
    def luck(self):
        return self._luck

    @luck.setter
    def luck(self, value):
        self._luck = round(max(0, min(value, 1)), 3)

    @property
    def stamina(self):
        if self.money < 1:
            return 0
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        self._stamina = round(max(0, min(value, 1)), 3)

    @property
    def dishonesty(self):
        return self._dishonesty

    @dishonesty.setter
    def dishonesty(self, value):
        self._dishonesty = round(max(0, min(value, 1)), 3)

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = round(max(0, value), 3)

    @property
    def bet(self):
        return 1 + par.theta * self.anxiety

    @property
    def activity_duration(self):
        return int((max(self.lucidity + self.sociability - self.anxiety,
                        0.1) * (m.pi ** 2)) * 60)

    def decide(self):
        if self.predict_rounds and (self.money >= self.bet):
            return 'p'
        retire = 1 - self.stamina
        play = min(self.anxiety, 1 - retire)
        activity = min(self.sociability, 1 - retire - play)
        installation = 1 - (retire + play + activity)
        return r.choices(['r', 'p', 'a', 'i'],
                         [retire, play, activity, installation])[0]

    def mafia(self):
        self.gangster = True
        self.money -= 20
        self.stamina -= par.eta

    def talk(self):
        self.anxiety *= 1 - par.epsilon/100
        self.dishonesty += par.chi
        self.social = True

    def predict(self):
        self.predict_rounds = r.choices([par.ny, 0], [self.dishonesty, 1 -
                                                      self.dishonesty])[0]
        if self.predict_rounds:
            self.cheat = True

    def wait(self, clients=None):
        if self.next_location in ('tini', 'talking', 'determinist'):
            self.wait_time -= 1
            if not self.wait_time:
                self.waiting = False
                if self.next_location == 'tini':
                    self.mafia()
                elif self.next_location == 'talking':
                    self.talk()
                else:
                    self.predict()
        elif self.next_location == 'talk':
            friends = [c for c in clients if
                       (c.next_location == 'talk') and c.waiting]
            if len(friends):
                self.next_location = 'meet'
                friends[0].waiting = False
                friends[0].next_location = self
                friends[0].walking = True
            else:
                self.wait_time -= 1
                if not self.wait_time:
                    self.waiting = False

    def walk(self, collisions):
        location = self.next_location
        if not self.aux_location:
            x, y = destiny(location, self)
            if (self.x == x) and (self.y == y):
                if location in ('tini', 'determinist'):
                    self.waiting = True
                    self.wait_time = self.activity_duration
                elif isinstance(location, Client):
                    self.waiting = True
                    self.next_location = 'talking'
                    location.next_location = 'talking'
                    talk_time = max(self.activity_duration,
                                    location.activity_duration)
                    self.wait_time = talk_time
                    location.wait_time = talk_time
                elif location == 'exit':
                    self.active = False
                    self.deleteLater()
                elif location == 'talk':
                    self.wait_time = int(par.delta * 60)
                    self.waiting = True
                else:
                    if location.active and (
                            len(location.queue) < location.max_queue):
                        self.next_location.queue.append(self)
                        self.busy = True
                self.next = None
                self.walking = False
            else:
                x0 = self.x
                y0 = self.y
                next_position, aux = paths(x0, y0, x, y, collisions)
                if aux:
                    self.aux_location = next_position
                    a1, a2 = next_position
                    next_position, aux = paths(x0, y0, a1, a2, collisions)
                x2, y2 = next_position
                self.x += x2 - self.x
                self.y += y2 - self.y
        else:
            x, y = self.aux_location
            x0 = self.x
            y0 = self.y
            if (self.x == x) and (self.y == y):
                self.aux_location = None
                x, y = destiny(location, self)
                next_position, aux = paths(x0, y0, x, y, collisions)
            else:
                next_position, aux = paths(x0, y0, x, y, collisions)
            x2, y2 = next_position
            self.x += x2 - self.x
            self.y += y2 - self.y


class Personnel:
    _id = 0

    def __init__(self, start_time):
        self.id = Personnel._id
        Personnel._id += 1
        self.name = n.get_full_name()
        self.age = r.randint(21, 60)
        self.working = False
        self.start_time = start_time
        self.stop_time = 0

    @property
    def rest_time(self):
        return int(max(8, min(r.normalvariate(14, 5), 20)))

    @property
    def work_time(self):
        return 0

    def start_turn(self):
        self.working = True
        work_time = self.work_time * 60
        self.stop_time = self.start_time + work_time

    def end_turn(self):
        self.working = False
        time = self.rest_time * 3600
        self.start_time = ((self.stop_time + time) // 3600) * 3600 + 3600
        if not ((self.stop_time + time) % 3600):
            self.start_time -= 3600


class Bartender(Personnel):
    def __init__(self, start_time):
        super().__init__(start_time)
        self.installation = 'restobar'

    @property
    def work_time(self):
        return int(r.triangular(360, 540, 490))


class MrT(Personnel):
    def __init__(self, start_time):
        super().__init__(start_time)
        self.installation = 'tarot'

    @property
    def work_time(self):
        return int(r.triangular(360, 500, 420))


class Dealer(Personnel):
    def __init__(self, start_time, gangster):
        super().__init__(start_time)
        self.installation = ('tragamonedas', 'ruleta')
        self.gangster = gangster

    @property
    def work_time(self):
        return int(r.triangular(360, 540, 540))


# Entrega los atributos según personalidad
def get_attributes(personality):
    attr_dict = {'ludopata': [1, 1, 2, 1, 1, 2, 1],
                 'kibitzer': [0, 2, 0, 1, 1, 0, 1],
                 'dieciochero': [1, 2, 2, 0, 1, 1, 0],
                 'ganador': [1, 2, 1, 1, 2, 2, 2],
                 'millonario': [2, 1, 1, 1, 1, 2, 1]}
    attr = []
    for att in attr_dict[personality]:
        if not att:
            attr.append(round(r.uniform(0, 0.299), 3))
        elif att == 1:
            attr.append(round(r.uniform(0.3, 0.699), 3))
        else:
            attr.append(round(r.uniform(0.7, 1), 3))
    return attr


# Entrega las coordenadas del próximo destino
def destiny(location, client):
    if not client.next:
        if location == 'tini':
            client.next = 720, 250
        elif location == 'determinist':
            client.next = 370, 340
        elif location == 'exit':
            client.next = 30, 8
        elif isinstance(location, Game):
            x, y = location.location
            if location.name == 'tragamonedas':
                if location.id == 0:
                    client.next = x + 149, r.randint(y, 432)
                else:
                    client.next = x - 35, r.randint(y, 432)
            else:
                client.next = r.choice([(
                                        r.randint(x, x + location.width() - 34),
                                        y + location.height() + 1), (
                                        x + location.width() + 1,
                                        r.randint(y + 5,
                                                  y + location.height() - 34))])
        elif isinstance(location, Building):
            x, y = location.location
            if location.name == 'restobar':
                client.next = r.choice([
                    (x - 35, r.randint(30, y + location.height() - 34)),
                    (x + location.width() + 1,
                     r.randint(30, y + location.height() - 34))])
            elif (location.id == 1) or (location.name == 'baños'):
                client.next = r.choice([
                    (x - 35, r.randint(30, y + location.height())),
                    (r.randint(x, x + location.width() - 34),
                     y + location.height() + 1),
                    (x + location.width() + 1,
                     r.randint(30, y + location.height()))])
            else:
                client.next = r.choice([
                    (x - 35, r.randint(y + 20, y + location.height())),
                    (r.randint(x, x + location.width() - 34),
                     y + location.height() + 1),
                    (x + location.width() + 1,
                     r.randint(y + 20, y + location.height()))])
        elif isinstance(location, Client):
            x = location.x + 20
            y = location.y
            client.next = x, y
    return client.next


# Algoritmo de movimiento y colisión de los clientes
def paths(x1, y1, x2, y2, collisions):
    options = list()
    options.append(distance(x1 + 1, y1, x2, y2))
    options.append(distance(x1 + 1, y1 + 1, x2, y2))
    options.append(distance(x1 + 1, y1 - 1, x2, y2))
    options.append(distance(x1, y1 + 1, x2, y2))
    options.append(distance(x1, y1 - 1, x2, y2))
    options.append(distance(x1 - 1, y1 - 1, x2, y2))
    options.append(distance(x1 - 1, y1 + 1, x2, y2))
    options.append(distance(x1 - 1, y1, x2, y2))
    s_options = sorted(options, key=lambda x: x[2])
    valid_paths = [(x[0], x[1]) for x in s_options]
    collision_paths = [x for x in valid_paths if (x not in collisions)
                       and (list(x)[0] <= 722) and (list(x)[1] <= 432) and
                       (list(x)[0] >= 18) and (list(x)[1] >= 8) and
                       ((list(x)[0] + 34, list(x)[1]) not in collisions) and
                       ((list(x)[0] + 34, list(x)[1] + 34) not in collisions)
                       and ((list(x)[0], list(x)[1] + 34) not in collisions)]
    if (valid_paths[0] in [(x1 + 1, y1), (x1 - 1, y1)]) and (
            valid_paths[0] != collision_paths[0]):
        if (list(valid_paths[0])[0], y1) in collisions:
            x = list(valid_paths[0])[0]
            y = y1
        elif (list(valid_paths[0])[0] + 34, y1) in collisions:
            x = list(valid_paths[0])[0] + 34
            y = y1
        elif (list(valid_paths[0])[0], y1 + 34) in collisions:
            x = list(valid_paths[0])[0]
            y = y1 + 34
        else:
            x = list(valid_paths[0])[0] + 34
            y = y1 + 34
        while (x, y) in collisions:
            y += 1
        return (x, y), True
    elif (valid_paths[0] in [(x1, y1 + 1), (x1, y1 - 1)]) and \
            (valid_paths[0] != collision_paths[0]):
        if (x1, list(valid_paths[0])[1]) in collisions:
            x = x1
            y = list(valid_paths[0])[1]
        elif (x1, list(valid_paths[0])[1] + 34) in collisions:
            x = x1
            y = list(valid_paths[0])[1] + 34
        elif (x1 + 34, list(valid_paths[0])[1]) in collisions:
            x = x1 + 34
            y = list(valid_paths[0])[1]
        else:
            x = x1 + 34
            y = list(valid_paths[0])[1] + 34
        while (x, y) in collisions:
            x += 1
        return (x, y), True
    return collision_paths[0], False


# Calcula la distancia entre 2 puntos
def distance(x1, y1, x2, y2):
    return [x1, y1, m.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))]
