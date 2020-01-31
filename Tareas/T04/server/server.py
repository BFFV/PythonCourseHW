import json
import pickle
from binascii import hexlify, unhexlify
from hashlib import sha256
from os import urandom
from os.path import exists
from math import sqrt
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from random import uniform, choice, randint
from PyQt5.QtCore import QRect

HOST = '127.0.0.1'
PORT = 8000


# Servidor del Juego
class GameServer:

    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.rooms = dict()
        self.clients = list()
        self.current_Id = 0
        accepting_thread = Thread(target=self.accept_connections, daemon=True)
        accepting_thread.start()

    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            receiving_thread = Thread(target=self.receive_request,
                                      args=(client_socket,), daemon=True)
            receiving_thread.start()

    def receive_request(self, client):
        while client in self.clients:
            request = ''
            try:
                bytes_length = client.recv(4)
                request_length = int.from_bytes(bytes_length, byteorder="big")
                request = bytearray()
                while len(request) < request_length:
                    request += client.recv(min(
                        4096, request_length - len(request)))
                message = pickle.loads(request)
                self.process_request(message, client)
            except pickle.UnpicklingError:
                decoded = request.decode(encoding='utf-8')
                message = json.loads(decoded)
                self.process_request(message, client)
            except ConnectionResetError:
                self.clients.remove(client)

    def process_request(self, message, client):
        if message['status'] == 'login':
            if self.check_database('login', message['data']):
                login_response = {'status': 'login', 'data': [
                    True, message['data']['user']]}
            else:
                login_response = {'status': 'login', 'data': [
                    False, message['data']['user']]}
            self.send(login_response, client, 'json')
        elif message['status'] == 'enter':
            self.find_room(client, message['data'])
        elif message['status'] == 'register':
            if self.check_database('register', message['data']):
                self.add_user(message['data'])
                registered_response = {'status': 'register', 'data': True}
            else:
                registered_response = {'status': 'register', 'data': False}
            self.send(registered_response, client, 'json')
        elif message['status'] == 'leave':
            room = self.rooms[message['data'][0]]
            if message['data'][1] and (len(room.clients) > 1):
                new_boss = room.clients[1]
                boss_response = {'status': 'new_boss', 'data': {}}
                self.send(boss_response, new_boss, 'json')
            index = room.clients.index(client)
            color = room.users[index][1]
            room.clients.remove(client)
            room.users.pop(index)
            room.colors.append(color)
            player_list_response = {'status': 'update_players',
                                    'data': room.users}
            room.update_players(player_list_response)
        elif message['status'] == 'color':
            room = self.rooms[message['data']['room']]
            if message['data']['new_color'] in room.colors:
                room.colors.remove(message['data']['new_color'])
                room.colors.append(message['data']['color'])
                index = room.clients.index(client)
                room.users[index][1] = message['data']['new_color']
                player_list_response = {'status': 'update_players',
                                        'data': room.users}
                room.update_players(player_list_response)
                color_response = {'status': 'color',
                                  'data': message['data']['new_color']}
            elif message['data']['color'] != message['data']['new_color']:
                color_response = {'status': 'color',
                                  'data': False}
            else:
                color_response = {'status': 'color',
                                  'data': message['data']['color']}
            if color_response:
                self.send(color_response, client, 'json')
        elif message['status'] == 'speed':
            room = self.rooms[message['data']['room']]
            room.speed = message['data']['speed']
            speed_response = {'status': 'speed', 'data': room.speed}
            room.update_players(speed_response)
        elif message['status'] == 'score':
            room = self.rooms[message['data']['room']]
            room.score = message['data']['score']
            score_response = {'status': 'score', 'data': room.score}
            room.update_players(score_response)
        elif message['status'] == 'power':
            room = self.rooms[message['data']['room']]
            if message['data']['active']:
                room.power_types.append(message['data']['power'])
            else:
                room.power_types.remove(message['data']['power'])
        elif message['status'] == 'playing':
            room = self.rooms[message['data']['room']]
            response = {'status': 'opponent_update', 'data': message['data']}
            room.update_players(response, client)
            room.check_powers(message['data'], client)
            if not message['data']['alive']:
                colors = ['red', 'blue', 'green', 'yellow']
                colors.remove(message['data']['color'])
                if message['data']['crash']:
                    index = 0
                    colors.remove(message['data']['crash'])
                    for user in room.users:
                        if user[1] == message['data']['crash']:
                            index = room.users.index(user)
                    crashed = room.clients[index]
                    crash_response = {'status': 'crash', 'data': True}
                    self.send(crash_response, crashed, 'pickle')
                room.set_scores(colors, message['data']['color'],
                                message['data']['crash'])
                if room.check_round():
                    room.spawn_timer.stop()
                    for power in room.powers:
                        room.delete_power(power)
                    room.powers = list()
                    freeze_response = {'status': 'freeze', 'data': True}
                    room.update_players(freeze_response)
                    for player in room.players:
                        player[3] = True
                    room.score_list = [[x[0], x[1], x[2]] for x in
                                       sorted(room.players,
                                              key=lambda x: x[2], reverse=True)]
                    print(room.score_list, room.score)
                    # enviar scores lista
                    """""
                    winner = None
                    if room.score_list[0][2] >= room.score:
                        winner = room.score_list[0][0]
                    elif (room.score_list[0][2] - room.score_list[1][2]) >= 2:
                        winner = room.score_list[0][0]
                    if winner:
                        index = 0
                        for user in room.users:
                            if user[0] == winner:
                                index = room.users.index(user)
                        win_response = {'status': 'win', 'data': True}
                        lost_response = {'status': 'win', 'data': False}
                        self.send(win_response, room.clients[index], 'pickle')
                        room.update_players(lost_response, room.clients[index])
                    """""
                    positions = room.get_positions()
                    interval = (1 - (room.speed / 100)) * 20 + 30
                    parameters_response = {'status': 'parameters', 'data': {
                        'interval': interval, 'positions': positions}}
                    room.update_players(parameters_response)
                    room.started = False
        elif message['status'] == 'chat':
            room = self.rooms[message['data']['room']]
            chat_response = {'status': 'chat', 'data': {
                'user': message['data']['user'],
                'text': message['data']['text']}}
            room.update_players(chat_response)
        elif message['status'] == 'try_playing':
            room = self.rooms[message['data']]
            try_response = {'status': 'try_playing', 'data': False}
            if len(room.clients) > 1:
                try_response = {'status': 'try_playing', 'data': True}
            self.send(try_response, client, 'json')
        elif message['status'] == 'countdown':
            room = self.rooms[message['data']]
            room.playing = True
            room.get_scores()
            count_response = {'status': 'countdown', 'data': True}
            positions = room.get_positions()
            interval = (1 - (room.speed / 100)) * 20 + 30
            parameters_response = {'status': 'parameters', 'data': {
                'interval': interval, 'positions': positions}}
            room.update_players(parameters_response)
            room.update_players(count_response)
        elif message['status'] == 'start':
            room = self.rooms[message['data']['room']]
            if not room.started:
                room.started = True
                # enviar score para ganar
                play_response = {'status': 'start_game', 'data': {}}
                room.update_players(play_response)
                room.init_spawn()
        elif message['status'] == 'pause':
            # power_pause
            room = self.rooms[message['data']['room']]
            pause_response = {'status': 'pause',
                              'data': message['data']['paused']}
            room.update_players(pause_response, 'pickle')
        elif message['status'] == 'exit':
            room = self.rooms[message['data']['room']]
            index = 0
            user = None
            if client in room.clients:
                index = room.clients.index(client)
                room.clients.remove(client)
            if index:
                user = room.users.pop(index)[0]
            for player in room.players:
                if player[0] == user:
                    room.players.remove(player)
            exit_response = {'status': 'exit',
                             'data': message['data']['action']}
            self.send(exit_response, client, 'pickle')
            if not len(room.clients):
                room.spawn_timer.stop()
                for power in room.powers:
                    room.delete_power(power)
                room.powers = list()
                room.started = False
                room.colors = ['red', 'blue', 'yellow', 'green']
                room.playing = False
                room.power_types = []
                room.speed = 50
                room.score = 20

    @staticmethod
    def send(response, client, serialization):
        if serialization == 'json':
            serialized = json.dumps(response)
            encoded = serialized.encode(encoding='utf-8')
        else:
            encoded = pickle.dumps(response, protocol=pickle.HIGHEST_PROTOCOL)
        bytes_length = len(encoded).to_bytes(4, byteorder="big")
        client.send(bytes_length + encoded)

    def find_room(self, client, user):
        response = None
        assigned = False
        for number in self.rooms:
            room = self.rooms[number]
            if not room.busy and not assigned:
                boss = not room.clients
                room.clients.append(client)
                color = choice(room.colors)
                room.colors.remove(color)
                room.users.append([user, color])
                assigned = True
                response = {'status': 'enter', 'data': {
                    'logged': True, 'room': number,
                    'boss': boss, 'user': user,
                    'color': color, 'speed': room.speed, 'score': room.score}}
                player_list_response = {'status': 'update_players',
                                        'data': room.users}
                room.update_players(player_list_response)
        if not assigned:
            self.rooms[self.current_Id] = \
                GameRoom(self, client, user)
            color = self.rooms[self.current_Id].users[0][1]
            response = {'status': 'enter', 'data': {
                'logged': True, 'room': self.current_Id, 'boss': True,
                'user': user, 'color': color}}
            room = self.rooms[self.current_Id]
            player_list_response = {'status': 'update_players',
                                    'data': room.users}
            room.update_players(player_list_response)
            self.current_Id += 1
        self.send(response, client, 'json')

    @staticmethod
    def check_database(option, data):
        if option == 'register':
            if not exists('database.json'):
                return True
            else:
                with open('database.json') as file:
                    users = json.load(file)
                    return data['user'] not in users
        else:
            if not exists('database.json'):
                return False
            else:
                with open('database.json') as file:
                    users = json.load(file)
                    if data['user'] not in users:
                        return False
                    salt = unhexlify(users[data['user']][0])
                    hashed = users[data['user']][1]
                    test_password = sha256(
                        salt + data['password'].encode()).hexdigest()
                    return hashed == test_password

    def add_user(self, data):
        if not exists('database.json'):
            with open('database.json', 'w') as file:
                users = dict()
                users[data['user']] = self.generate_password(data['password'])
                json.dump(users, file)
        else:
            with open('database.json') as file:
                users = json.load(file)
                users[data['user']] = self.generate_password(data['password'])
            with open('database.json', 'w') as file:
                json.dump(users, file)

    @staticmethod
    def generate_password(password):
        salt = urandom(8)
        byte_password = password.encode()
        new_password = salt + byte_password
        encrypted = sha256(new_password).hexdigest()
        string_salt = hexlify(salt).decode()
        return [string_salt, encrypted]


class TimerThread(Thread):

    def __init__(self, target, interval):
        super().__init__()
        self.interval = interval
        self.target = target
        self.active = True

    def stop(self):
        self.active = False

    def run(self):
        while self.active:
            sleep(self.interval)
            if self.active:
                self.target()


class GameRoom:
    def __init__(self, server, client=None, user=None):
        super().__init__()
        self.colors = ['red', 'blue', 'yellow', 'green']
        self.playing = False
        self.started = False
        self.clients = list()
        self.users = list()
        self.players = list()
        self.score_list = list()
        if client:
            self.clients.append(client)
        if user:
            color = choice(self.colors)
            self.colors.remove(color)
            self.users.append([user, color])
        self.server = server
        self.powers = list()
        self.power_types = []
        self.spawn_timer = None
        self.speed = 50
        self.score = 20

    @property
    def busy(self):
        if len(self.clients) >= 4:
            return True
        return self.playing

    def init_spawn(self):
        self.spawn_timer = TimerThread(self.spawn_powers, uniform(5, 10))
        self.spawn_timer.start()

    def spawn_powers(self):
        if self.power_types:
            new_power = Power(self, choice(self.power_types))
            self.powers.append(new_power)
            spawn_response = {'status': 'spawn_power', 'data': {
                'id': new_power.id, 'x': new_power.x, 'y': new_power.y,
                'name': new_power.name}}
            self.update_players(spawn_response)
            self.spawn_timer.interval = uniform(5, 10)

    def delete_power(self, power):
        if power in self.powers:
            self.powers.remove(power)
        delete_response = {'status': 'delete_power', 'data': power.id}
        self.update_players(delete_response)

    def update_players(self, response, client=None):
        for player in self.clients:
            if player != client:
                self.server.send(response, player, 'pickle')

    def check_powers(self, data, client):
        client_rect = QRect(data['x'], data['y'], 18, 18)
        for power in self.powers:
            if not power.affected:
                if client_rect.intersects(power.rect):
                    power.affected = client
                    power.color = data['color']
                    self.delete_power(power)
                    power.effect()

    def get_positions(self):
        positions = dict()
        for client in self.clients:
            index = self.clients.index(client)
            bad = True
            while bad:
                bad = False
                x = randint(2, 680)
                y = randint(2, 580)
                angle = randint(0, 360)
                if x > 630:
                    angle = 180
                elif x < 50:
                    angle = 0
                elif y > 530:
                    angle = 90
                elif y < 50:
                    angle = 270
                for position in positions:
                    if self.distance(x, y, positions[position][0],
                                     positions[position][1]):
                        bad = True
                if not bad:
                    positions[self.users[index][1]] = [x, y, angle]
        return positions

    def get_scores(self):
        for user in self.users:
            self.players.append(user + [0, True, 0])

    def set_scores(self, winners, loser, crash):
        if crash:
            loser_player = None
            for player in self.players:
                if player[1] == loser:
                    loser_player = player
            for player in self.players:
                if (player[1] == crash) and player[3]:
                    player[3] = False
                    if loser_player[2] > player[2]:
                        player[2] += 1
                    elif loser_player[2] == player[2]:
                        if loser_player[4] >= player[4]:
                            loser_player[2] += 1
                        else:
                            player[2] += 1
                    else:
                        loser_player[2] += 1
        for player in self.players:
            if player[1] == loser:
                player[3] = False
            elif player[3] and (player[1] in winners):
                player[2] += 1

    @staticmethod
    def distance(x, y, x0, y0):
        return sqrt((x - x0) ** 2 + (y - y0) ** 2) < 50

    def check_round(self):
        count = 0
        for player in self.players:
            if player[3]:
                count += 1
        return count <= 1


class Power:

    _id = 0

    def __init__(self, parent, name):
        self.id = Power._id
        Power._id += 1
        self.parent = parent
        self.name = name
        self.effect_timer = None
        self.affected = None
        self.active_timer = TimerThread(self.end, 6)
        self.remaining = 0
        self.x = randint(1, 660)
        self.y = randint(1, 560)
        self.rect = QRect(self.x, self.y, 40, 40)
        self.active_timer.start()

    def effect(self):
        duration = 0
        if self.name == 'speed':
            effect_response = {'status': 'effect', 'data': 'speed',
                               'activate': True}
            self.parent.server.send(effect_response, self.affected, 'pickle')
            duration = 5
        elif self.name == 'clean':
            effect_response = {'status': 'effect', 'data': 'clean',
                               'activate': True}
            self.parent.update_players(effect_response)
        elif self.name == 'beer':
            effect_response = {'status': 'effect', 'data': 'drunk',
                               'ID': self.id, 'activate': True}
            self.parent.server.send(effect_response, self.affected, 'pickle')
            duration = 5
        elif self.name == 'nebcoin':
            index = self.parent.clients.index(self.affected)
            color = self.parent.users[index][1]
            for player in self.parent.players:
                if player[1] == color:
                    player[4] += 1
        elif self.name == 'three':
            for n in range(3):
                self.parent.spawn_powers()
        elif self.name == 'sleep':
            effect_response = {'status': 'effect', 'data': 'sleep',
                               'activate': True}
            self.parent.server.send(effect_response, self.affected, 'pickle')
            duration = 5
        elif self.name == 'collide':
            effect_response = {'status': 'effect', 'data': 'ghost',
                               'ID': self.id, 'activate': True}
            self.parent.server.send(effect_response, self.affected, 'pickle')
            duration = 4
        elif self.name == 'teleport':
            effect_response = {'status': 'effect', 'data': 'teleport',
                               'ID': self.id, 'activate': True}
            self.parent.update_players(effect_response)
            duration = 8
        elif self.name == 'tau':
            effect_response = {'status': 'effect', 'data': 'tau',
                               'ID': self.id, 'activate': True}
            self.parent.server.send(effect_response, self.affected, 'pickle')
            duration = 6
        self.effect_timer = TimerThread(self.deactivate_effect, duration)
        self.effect_timer.start()

    def deactivate_effect(self):
        if self.name == 'speed':
            deactivate_response = {'status': 'effect', 'data': 'sleep',
                                   'activate': False}
            self.parent.server.send(
                deactivate_response, self.affected, 'pickle')
        elif self.name == 'beer':
            deactivate_response = {'status': 'effect', 'data': 'sober',
                                   'ID': self.id, 'activate': False}
            self.parent.server.send(
                deactivate_response, self.affected, 'pickle')
        elif self.name == 'sleep':
            deactivate_response = {'status': 'effect', 'data': 'speed',
                                   'activate': False}
            self.parent.server.send(
                deactivate_response, self.affected, 'pickle')
        elif self.name == 'collide':
            deactivate_response = {'status': 'effect', 'data': 'solid',
                                   'ID': self.id, 'activate': False}
            self.parent.server.send(
                deactivate_response, self.affected, 'pickle')
        elif self.name == 'teleport':
            deactivate_response = {'status': 'effect', 'data': 'borders',
                                   'ID': self.id, 'activate': False}
            self.parent.update_players(deactivate_response)
        elif self.name == 'tau':
            deactivate_response = {'status': 'effect', 'data': 'pi',
                                   'ID': self.id, 'activate': False}
            self.parent.server.send(
                deactivate_response, self.affected, 'pickle')
        self.effect_timer.stop()

    def end(self):
        if not self.affected:
            self.parent.delete_power(self)
        self.active_timer.stop()


if __name__ == "__main__":
    game_server = GameServer()
    while True:
        pass
