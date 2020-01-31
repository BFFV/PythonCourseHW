from people import Client, Bartender, MrT, Dealer
from services import Bar, Tarot, Bath, SlotMachine, Roulette
import gui
import random as r
import sys
import statistics as s
import parameters as par


class Simulation:
    def __init__(self, max_time, delay):
        self.timer = 0
        self.clients = []
        self.installations = []
        self.personnel = []
        self.games = []
        self.past_clients = []
        self.collisions = []
        self.max_time = max_time
        self.delay = delay

    def tick(self):
        if self.timer == self.max_time:
            self.statistics()
            sys.exit()
        spawn = r.choices([True, False], [par.p, 1 - par.p])[0]
        if spawn:
            personality = r.choice(
                ['ludopata', 'kibitzer', 'ganador', 'millonario',
                 'dieciochero'])
            client = Client(personality, 30, 8)
            self.clients += [client]
            gui.add_entity(client)
            client.setFixedSize(34, 34)
        personnel_tick(self.timer, self.personnel, self.installations,
                       self.games)
        installation_use(self.installations)
        play_games(self.games)
        self.clients = client_tick(self.clients, self.installations, self.games,
                                   self.past_clients, self.collisions)
        installation_entry(self.installations)
        game_entry(self.games)
        self.timer += 1

    def run(self):
        gui.init()
        gui.set_size(773, 485)
        time = 0
        for person in range(11):
            for n in range(5):
                self.personnel.append(Bartender(time))
            time = r.randint(0, 36000)
        self.personnel += [MrT(0), MrT(36000), MrT(r.randint(0, 61200))]
        self.installations += [Bar('restobar', 300, 13),
                               Tarot('tarot', 150, 15), Tarot('tarot', 60, 200),
                               Tarot('tarot', 580, 130), Bath('baños', 520, 18),
                               Bath('baños', 650, 18)]
        for inst in self.installations:
            gui.add_entity(inst)
            inst.updatePixmap()
            self.collisions += [(x, inst.y) for x in
                                range(inst.x, inst.x + inst.width() + 1)]
            self.collisions += [(x, inst.y + inst.height()) for x in
                                range(inst.x, inst.x + inst.width() + 1)]
            self.collisions += [(inst.x, y) for y in
                                range(inst.y, inst.y + inst.height() + 1)]
            self.collisions += [(inst.x + inst.width(), y) for y in
                                range(inst.y, inst.y + inst.height() + 1)]
        for dealer in range(15):
            self.personnel.append(Dealer(0, False))
            self.personnel.append(Dealer(25200, False))
            self.personnel.append(Dealer(50400, False))
            self.personnel.append(Dealer(r.randint(0, 50400), True))
        for dealer in range(2):
            self.personnel.append(Dealer(36000, True))
        self.games += [SlotMachine('tragamonedas', 18, 342),
                       SlotMachine('tragamonedas', 608, 342),
                       Roulette('ruleta', 250, 280),
                       Roulette('ruleta', 425, 280),
                       Roulette('ruleta', 250, 380),
                       Roulette('ruleta', 425, 380)]
        for game in self.games:
            gui.add_entity(game)
            game.updatePixmap()
            self.collisions += [(x, game.y) for x in
                                range(game.x, game.x + game.width() + 1)]
            self.collisions += [(x, game.y + game.height()) for x in
                                range(game.x, game.x + game.width() + 1)]
            self.collisions += [(game.x, y) for y in
                                range(game.y, game.y + game.height() + 1)]
            self.collisions += [(game.x + game.width(), y) for y in
                                range(game.y, game.y + game.height() + 1)]
        self.collisions = set(self.collisions)
        gui.run(self.tick, self.delay)

    def statistics(self):
        data = open('Statistics.txt', 'w', encoding='utf-8')
        print('Estadísticas:\n')
        data.write('Estadísticas:\n')
        client_money = [(x.money - x.wealth * 200) for x in self.clients] + [
            (x.money - x.wealth * 200) for x in self.past_clients]
        print(f'Ganancia Promedio Final por Cliente: {s.mean(client_money)}\n')
        data.write(f'\nGanancia Promedio Final por Cliente: '
                   f'{s.mean(client_money)}\n')
        pers_money = []
        for personality in ['ludopata', 'kibitzer', 'dieciochero', 'ganador',
                            'millonario']:
            pers = [(x.money - x.wealth * 200) for x in self.clients if
                    x.personality == personality] + [
                       (x.money - x.wealth * 200) for x in
                       self.past_clients if x.personality == personality]
            pers_money.append([personality, s.mean(pers)])
        print('Ganancia Promedio Final por Personalidad:\n')
        data.write('\nGanancia Promedio Final por Personalidad:\n')
        for p in pers_money:
            print(f'{p[0]}: {p[1]}\n')
            data.write(f'{p[0]}: {p[1]}\n')
        client_time = [x.time for x in self.clients] + \
                      [x.time for x in self.past_clients]
        print(f'Tiempo Promedio de Estadía por Cliente: '
              f'{s.mean(client_time) / 60} Minutos\n')
        data.write(f'\nTiempo Promedio de Estadía por '
                   f'Cliente: {s.mean(client_time) / 60} Minutos\n')
        pers_time = []
        for personality in ['ludopata', 'kibitzer', 'dieciochero', 'ganador',
                            'millonario']:
            pers = [x.time for x in self.clients if x.personality ==
                    personality] + [x.time for x in self.past_clients
                                    if x.personality == personality]
            pers_time.append([personality, s.mean(pers)])
        print('Tiempo Promedio de Estadía por Personalidad:\n')
        data.write('\nTiempo Promedio de Estadía por Personalidad:\n')
        for p in pers_time:
            print(f'{p[0]}: {p[1] / 60} Minutos\n')
            data.write(f'{p[0]}: {p[1] / 60} Minutos\n')
        days = self.max_time / 86400
        earnings = 0
        for game in self.games:
            if game.name == 'tragamonedas':
                earnings += game.pit
            earnings += game.earnings
        for inst in self.installations:
            earnings += inst.earnings
        print(f'Ganancia Promedio del Casino por Día: {earnings / days}\n')
        data.write(
            f'\nGanancia Promedio del Casino por Día: {earnings / days}\n')
        slot_wins = sum([(x.earnings + x.pit - x.prize) for x in self.games if
                         x.name == 'tragamonedas'])
        roulette_wins = sum([x.earnings for x in self.games if
                             x.name == 'ruleta'])
        best_game = max(['Tragamonedas', slot_wins], ['Ruleta', roulette_wins],
                        key=lambda x: x[1])
        print(f'Juego que Generó Mayor Ganancia Neta: Juego: {best_game[0]}, '
              f'Ganancia: {best_game[1]}\n')
        data.write(f'\nJuego que Generó Mayor Ganancia Neta: '
                   f'Juego: {best_game[0]}, Ganancia: {best_game[1]}\n')
        total_clients = len(self.clients + self.past_clients)
        cheaters = len([x for x in self.clients if x.cheat] +
                       [x for x in self.past_clients if x.cheat])
        print('Porcentaje de Clientes que Contó Cartas: '
              + str((cheaters / total_clients) * 100) + ' %\n')
        data.write('\nPorcentaje de Clientes que Contó Cartas: ' +
                   str((cheaters / total_clients) * 100) + ' %\n')
        expelled = len([x for x in self.past_clients if x.expelled])
        retired = len([x for x in self.past_clients
                       if (not x.expelled) and x.stamina])
        broke = len([x for x in self.past_clients
                     if (not x.expelled) and (not x.stamina)])
        total_past = len(self.past_clients)
        print('Razones de Salida del Casino:\n')
        data.write('\nRazones de Salida del Casino:\n')
        for reasons in [['Motivos Personales', (retired / total_past) * 100],
                        ['Sin Dinero', (broke / total_past) * 100],
                        ['Expulsado', (expelled / total_past) * 100]]:
            data.write(f'{reasons[0]}: {reasons[1]} %\n')
            print(f'{reasons[0]}: {reasons[1]} %')
        print('\nTiempo Total Sin Funcionar de Cada Instalación:\n')
        data.write('\nTiempo Total Sin Funcionar de Cada Instalación:\n')
        for inst in self.installations:
            print(f'Instalación: {inst.name}, Id: {inst.id}, '
                  f'Tiempo de Inactividad: {inst.inactive_time / 3600} Horas')
            data.write(f'Instalación: {inst.name}, Id: {inst.id}, '
                       f'Tiempo de '
                       f'Inactividad: {inst.inactive_time / 3600} Horas\n')
        print('\nNúmero de Visitas a cada Juego en '
              'Promedio por Día:\n')
        data.write('\nNúmero de Visitas a cada Juego en '
                   'Promedio por Día:\n')
        slot_visits = sum([x.visits for x in self.games
                           if x.name == 'tragamonedas'])
        roulette_visits = sum([x.visits for x in self.games
                               if x.name == 'ruleta'])
        data.write(f'Ruleta: {roulette_visits / days}\n'
                   f'Tragamonedas: {slot_visits / days}')
        print(f'Ruleta: {roulette_visits / days}\n'
              f'Tragamonedas: {slot_visits / days}')
        data.close()


# Tick del personal del casino
def personnel_tick(timer, personnel, installations, games):
    for inst in installations:
        for person in inst.workers:
            if person.stop_time == timer:
                person.end_turn()
        inst.workers = [x for x in inst.workers if x.working]
    for person in personnel:
        if (not person.working) and (person.start_time == timer):
            if person.installation == 'restobar':
                person.start_turn()
                bar_list = [x for x in installations if x.name == 'restobar']
                r.choice(bar_list).workers.append(person)
            elif person.installation == 'tarot':
                person.start_turn()
                tarot_list = [x for x in installations if
                              x.name == 'tarot' and not len(x.workers)]
                r.choice(tarot_list).workers.append(person)
            else:
                person.start_turn()
                sorted(games, key=lambda y: len(y.dealers))[0].dealers.append(
                    person)


# Tick de uso de las instalaciones (clientes que ya entraron)
def installation_use(installations):
    for inst in installations:
        if inst.active:
            inst.use()
        else:
            inst.inactive_time += 1
            inst.close()


# Tick de entrada a las instalaciones (clientes en la fila de espera)
def installation_entry(installations):
    for inst in installations:
        if inst.active:
            inst.enter()


# Tick de uso de los juegos (clientes que ya entraron)
def play_games(games):
    for game in games:
        if game.active:
            game.play()
        else:
            game.close()


# Tick de entrada a los juegos (clientes en la fila de espera)
def game_entry(games):
    for game in games:
        if game.active:
            game.enter()


# Tick de los clientes
def client_tick(clients, installations, games, past, collisions):
    for client in clients:
        if client.expelled and (not client.walking):
            past.append(client)
            client.next_location = 'exit'
            client.walking = True
        if client.walking:
            client.walk(collisions)
            client.time += 1
        elif client.waiting:
            if client.next_location == 'talk':
                client.wait([x for x in clients if x != client])
            else:
                client.wait()
            client.time += 1
        elif not client.busy:
            client.time += 1
            decision = client.decide()
            if decision == 'r':
                past.append(client)
                client.next_location = 'exit'
                client.walking = True
                client.walk(collisions)
            elif decision == 'p':
                if client.predict_rounds and (client.money >= client.bet):
                    choice = r.choice([x for x in games if x.name == 'ruleta'])
                else:
                    choice = r.choice(games)
                if client.money >= client.bet:
                    client.next_location = choice
                    client.walking = True
                    client.walk(collisions)
            elif decision == 'i':
                choice = r.choice(installations)
                if client.money >= choice.cost:
                    client.next_location = choice
                    client.walking = True
                    client.walk(collisions)
            else:
                choice = r.choice(['t', 'g', 'd'])
                if choice == 't':
                    client.next_location = 'talk'
                    client.next = r.choice(
                        [(r.randint(168, 500), r.randint(210, 230)),
                         (r.randint(30, 90), r.randint(120, 150))])
                    client.walking = True
                    client.walk(collisions)
                elif choice == 'g':
                    if client.money >= 20:
                        client.next_location = 'tini'
                        client.walking = True
                        client.walk(collisions)
                else:
                    if (client.personality == 'kibitzer') and client.social:
                        client.next_location = 'determinist'
                        client.walking = True
                        client.walk(collisions)
    return [x for x in clients if x.active]
