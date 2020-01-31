from gui.entities import Building, Game
from collections import deque
import random as r
import parameters as par


class Installation(Building):
    _id = 0

    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.id = Installation._id
        Installation._id += 1
        self.location = (x, y)
        self.name = name
        self.queue = deque()
        self._active = False
        self.inactive_time = 0
        self.max_cap = 0
        self.max_queue = par.max_queue
        self.cost = 0
        self.min_personnel = 0
        self.workers = []
        self.clients = []
        self.earnings = 0

    @property
    def active(self):
        self._active = len(self.workers) >= self.min_personnel
        return self._active

    @property
    def duration(self):
        return 0

    def use(self):
        for client in self.clients:
            client[1] -= 1
            if not client[1]:
                client[0].busy = False
                interact(client[0], self.name)
        self.clients = [x for x in self.clients if x[0].busy]

    def enter(self):
        capacity = self.max_cap - len(self.clients)
        duration = self.duration
        for i in range(min(capacity, len(self.queue))):
            client = self.queue.popleft()
            client.money -= self.cost
            self.earnings += self.cost
            self.clients.append([client, duration])

    def close(self):
        for client in self.clients:
            client[0].busy = False
        for client in self.queue:
            client.busy = False
        self.clients = []
        self.queue = deque()


class Bar(Installation):
    def __init__(self, *args):
        super().__init__(*args)
        self.max_cap = 20
        self.cost = 2
        self.min_personnel = 2

    @property
    def duration(self):
        return max(52 - len(self.workers), 10) * 60


class Tarot(Installation):
    def __init__(self, *args):
        super().__init__(*args)
        self.max_cap = 1
        self.cost = 10
        self.min_personnel = 1

    @property
    def duration(self):
        return max(1, int(r.normalvariate(3, 5) * 60))


class Bath(Installation):
    def __init__(self, *args):
        super().__init__(*args)
        self.max_cap = 20
        self.cost = 0.2
        self.min_personnel = 0

    @staticmethod
    def client_duration(client):
        return max(1, int(r.normalvariate(3 * (1 - client.lucidity), 2) * 60))

    def enter(self):
        capacity = self.max_cap - len(self.clients)
        for i in range(min(capacity, len(self.queue))):
            client = self.queue.popleft()
            client.money -= self.cost
            self.clients.append([client, self.client_duration(client)])


class Games(Game):
    _id = 0

    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.id = Games._id
        Games._id += 1
        self.location = (x, y)
        self.name = name
        self.queue = deque()
        self._active = False
        self.max_cap = 0
        self.max_queue = par.max_queue
        self.duration = r.randint(300, 1800)
        self.dealers = []
        self.clients = []
        self.earnings = 0
        self.visits = 0
        self.probability = 0

    @property
    def active(self):
        self._active = len(self.dealers) >= 1
        return self._active

    def game_probability(self, choice=None):
        if not choice:
            return self.probability

    def win_probability(self, client):
        return max(min(self.game_probability() + 0.2 * client.luck - 0.1, 1), 0)

    def gamble(self, client):
        return self, client

    def play(self):
        for client in self.clients:
            client[1] -= 1
            if not client[1]:
                client[0].busy = False
                self.gamble(client[0])
        self.clients = [x for x in self.clients if x[0].busy]

    def enter(self):
        capacity = self.max_cap - len(self.clients)
        duration = self.duration
        for i in range(min(capacity, len(self.queue))):
            client = self.queue.popleft()
            self.clients.append([client, duration])
            self.visits += 1

    def close(self):
        for client in self.clients:
            client[0].busy = False
        for client in self.queue:
            client.busy = False
        self.clients = []
        self.queue = deque()


class SlotMachine(Games):
    def __init__(self, *args):
        super().__init__(*args)
        self.max_cap = 1
        self.pit = 0
        self.prize = 0
        self.probability = par.alpha

    def gamble(self, client):
        bet = client.bet
        client.money -= bet
        self.pit += 0.9 * bet
        self.earnings += 0.1 * bet
        probability = self.win_probability(client)
        choice = r.choices(['w', 'l'], [probability, 1 - probability])[0]
        if choice == 'w':
            client.money += self.pit
            self.prize += self.pit
            self.pit = 0


class Roulette(Games):
    def __init__(self, *args):
        super().__init__(*args)
        self.max_cap = 5
        self.number = par.gamma

    def game_probability(self, choice=None):
        if choice in ('g', 'n'):
            return 1 / (self.number + 1)
        if choice in ('b', 'r'):
            return self.number / (2 * (self.number + 1))

    def win_roulette(self, client, choice):
        return max(
            min(self.game_probability(choice) + 0.2 * client.luck - 0.1, 1), 0)

    def gamble(self, client):
        bet = client.bet
        option = r.choices(['n', 'r', 'b', 'g'], [0.5, 0.17, 0.17, 0.16])[0]
        probability = self.win_roulette(client, option)
        if client.gangster and (len([x for x in self.dealers if x.gangster])):
            probability = min(probability * (1 + par.kappa/100), 1)
        if client.predict_rounds:
            client.predict_rounds -= 1
            probability = min(probability * (1 + par.psi/100), 1)
            expel = min(len(self.dealers) * par.omega, 1)
            client.expelled = r.choices([False, True], [1 - expel, expel])[0]
        if not client.expelled:
            choice = r.choices(['w', 'l'], [probability, 1 - probability])[0]
            if (choice == 'w') and (option in ('n', 'g')):
                client.money += 5 * bet
                self.earnings -= 5 * bet
            elif (choice == 'w') and (option in ('r', 'b')):
                client.money += 1.5 * bet
                self.earnings -= 1.5 * bet
            else:
                client.money -= bet
                self.earnings += bet


# Interacción cliente - instalación
def interact(client, installation):
    if installation == 'restobar':
        if client.lucidity > client.anxiety:
            choice = 'd'
        elif client.lucidity < client.anxiety:
            choice = 'e'
        else:
            choice = r.choice(['d', 'e'])
        if choice == 'd':
            client.lucidity -= 0.2
            client.anxiety -= 0.15
            client.stamina += 0.3
        else:
            client.lucidity += 0.1
            client.anxiety -= 0.2
    elif installation == 'tarot':
        choice = r.choice(['g', 'b'])
        if choice == 'g':
            client.luck += 0.2
        else:
            client.stamina -= 0.2
    else:
        client.anxiety -= 0.1
