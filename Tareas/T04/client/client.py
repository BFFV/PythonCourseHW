import json
import pickle
from collections import deque
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

HOST = '127.0.0.1'
PORT = 8000


# Cliente
class Client:

    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.busy = False
        self.connected = False
        self.opponent_list = list()
        self.opponents = dict()
        self.user = None
        self.member = None
        self.player = None
        while not self.connected:
            try:
                self.client_socket.connect((self.host, self.port))
                self.connected = True
                receiving_thread = Thread(target=self.receive_response,
                                          daemon=True)
                receiving_thread.start()
            except ConnectionRefusedError:
                print('Esperando al Servidor...')

    def set_opponents(self, opponents):
        for opponent in opponents:
            self.opponent_list.append(opponent)

    def receive_response(self):
        while self.connected:
            response = ''
            try:
                bytes_length = self.client_socket.recv(4)
                response_length = int.from_bytes(bytes_length, byteorder="big")
                response = bytearray()
                while len(response) < response_length:
                    response += self.client_socket.recv(min(
                        4096, response_length - len(response)))
                message = pickle.loads(response)
                self.process_response(message)
            except pickle.UnpicklingError:
                decoded = response.decode(encoding='utf-8')
                message = json.loads(decoded)
                self.process_response(message)
            except ConnectionResetError:
                self.disconnect()

    def process_response(self, message):
        if message['status'] == 'login':
            self.user.name = message['data'][1]
            self.user.check_signal.emit(message['data'][0])
        elif message['status'] == 'enter':
            if message['data']['logged']:
                self.player.color = message['data']['color']
                self.member.color = message['data']['color']
                self.member.room = message['data']['room']
                self.member.boss = message['data']['boss']
                self.member.name = message['data']['user']
            self.user.room_signal.emit(message['data']['logged'])
            if not message['data']['boss']:
                self.member.default_signal.emit(message['data'])
        elif message['status'] == 'register':
            self.user.registered_signal.emit(message['data'])
        elif message['status'] == 'new_boss':
            self.member.boss = True
            self.member.custom_signal.emit(True)
        elif message['status'] == 'update_players':
            self.member.player_list_signal.emit(message['data'])
        elif message['status'] == 'color':
            if not message['data']:
                self.member.color_signal.emit(False)
            else:
                self.member.color = message['data']
                self.player.color = message['data']
                self.member.color_signal.emit(True)
        elif message['status'] == 'chat':
            text = f"{message['data']['user']}: {message['data']['text']}\n"
            self.member.message_signal.emit(text)
        elif message['status'] == 'speed':
            self.member.show_speed_signal.emit(str(message['data']))
        elif message['status'] == 'score':
            self.member.show_score_signal.emit(str(message['data']))
        elif message['status'] == 'room':
            self.player.room = message['data']
        elif message['status'] == 'opponent_update':
            opponent_status = message['data']
            opponent = self.opponents[opponent_status['color']]
            opponent.x = opponent_status['x']
            opponent.y = opponent_status['y']
            opponent.angle = opponent_status['angle']
            opponent.direction = opponent_status['direction']
            opponent.alive = opponent_status['alive']
            opponent.trail = opponent_status['trail']
            opponent.solid = opponent_status['solid']
            opponent.inverted = opponent_status['inverted']
            opponent.tau = opponent_status['tau']
            opponent.angle_var = opponent_status['angle_var']
            opponent.teleport = opponent_status['teleport']
            opponent.move()
        elif message['status'] == 'start_game':
            self.member.game_signal.emit(True)
        elif message['status'] == 'spawn_power':
            self.player.power_signal.emit(message['data'])
        elif message['status'] == 'delete_power':
            self.player.delete_power_signal.emit(message['data'])
        elif message['status'] == 'effect':
            if message['activate'] and self.player.immune:
                self.player.immune = False
            if not self.player.immune:
                if message['data'] == 'speed':
                    self.player.interval /= 2
                elif message['data'] == 'sleep':
                    self.player.interval *= 2
                elif message['data'] == 'drunk':
                    self.player.inverted = [True, message['ID']]
                elif message['data'] == 'sober':
                    if self.player.inverted[1] == message['ID']:
                        self.player.inverted = [False, None]
                elif message['data'] == 'ghost':
                    self.player.solid = [False, message['ID']]
                elif message['data'] == 'solid':
                    if self.player.solid[1] == message['ID']:
                        self.player.solid = [True, None]
                        self.player.safe_trail = deque()
                elif message['data'] == 'clean':
                    self.player.collisions_list = []
                    self.player.clean_signal.emit(True)
                elif message['data'] == 'teleport':
                    self.player.teleport = [True, message['ID']]
                elif message['data'] == 'borders':
                    if self.player.teleport[1] == message['ID']:
                        self.player.teleport = [False, None]
                elif message['data'] == 'tau':
                    self.player.angle_var = 90
                    self.player.tau_id = message['ID']
                elif message['data'] == 'pi':
                    if self.player.tau_id == message['ID']:
                        self.player.angle_var = 6
        elif message['status'] == 'try_playing':
            self.member.play_signal.emit(message['data'])
        elif message['status'] == 'parameters':
            for color in message['data']['positions']:
                index = 0
                position = message['data']['positions'][color]
                if color == self.player.color:
                    self.player.x = position[0]
                    self.player.y = position[1]
                    self.player.angle = position[2]
                    self.player.set_up()
                else:
                    opponent = self.opponent_list[index]
                    opponent.x = position[0]
                    opponent.y = position[1]
                    opponent.angle = position[2]
                    opponent.set_up(color)
                    self.opponents[opponent.color] = opponent
                    index += 1
            self.player.interval = message['data']['interval']
            self.player.set_up_signal.emit(message['data']['positions'])
        elif message['status'] == 'countdown':
            self.member.countdown_signal.emit('')
        elif message['status'] == 'crash':
            if self.player.alive:
                self.player.alive = False
        elif message['status'] == 'freeze':
            self.player.freeze()
        elif message['status'] == 'pause':
            self.player.paused_signal.emit(message['data'])
        elif message['status'] == 'exit':
            if message['data'] == 'exit':
                self.user.reset_signal.emit(True)
            else:
                enter_request = {'status': 'enter', 'data': self.user.name}
                self.send(enter_request, 'json')
                self.player.close_signal.emit(True)
        elif message['status'] == 'win':
            self.player.label_signal.emit(message['data'])

    def send(self, request, serialization):
        if serialization == 'json':
            serialized = json.dumps(request)
            encoded = serialized.encode(encoding='utf-8')
        else:
            encoded = pickle.dumps(request, protocol=pickle.HIGHEST_PROTOCOL)
        bytes_length = len(encoded).to_bytes(4, byteorder="big")
        self.client_socket.send(bytes_length + encoded)

    def disconnect(self):
        self.connected = False
        self.client_socket.close()
