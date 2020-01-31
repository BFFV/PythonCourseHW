import math as m
from collections import deque
from time import sleep
from random import uniform, choice, randint
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRect


# Lógica de la Ventana de Inicio
class User(QObject):

    check_signal = pyqtSignal(bool)
    bad_confirmation_signal = pyqtSignal(bool)
    registered_signal = pyqtSignal(bool)
    room_signal = pyqtSignal(bool)
    reset_signal = pyqtSignal(bool)

    def __init__(self, parent, client):
        super().__init__()
        self.client = client
        self.client.user = self
        self.name = ''
        self.check_signal.connect(parent.login)
        self.bad_confirmation_signal.connect(parent.bad_confirmation)
        self.registered_signal.connect(parent.registered)
        self.room_signal.connect(parent.assigned)
        self.reset_signal.connect(parent.reset)

    def register(self, event):
        if event[1] != event[2]:
            self.bad_confirmation_signal.emit(True)
        else:
            register_request = {'status': 'register', 'data': {
                'user': event[0], 'password': event[1]}}
            self.client.send(register_request, 'json')

    def login(self, event):
        login_request = {'status': 'login', 'data': {
            'user': event[0], 'password': event[1]}}
        self.client.send(login_request, 'json')

    def enter_lobby(self, event):
        if event:
            enter_request = {'status': 'enter', 'data': self.name}
            self.client.send(enter_request, 'json')


# Lógica de la Sala de Espera
class Member(QObject):

    message_signal = pyqtSignal(str)
    game_signal = pyqtSignal(bool)
    custom_signal = pyqtSignal(bool)
    player_list_signal = pyqtSignal(list)
    color_signal = pyqtSignal(bool)
    show_speed_signal = pyqtSignal(str)
    show_score_signal = pyqtSignal(str)
    play_signal = pyqtSignal(bool)
    countdown_signal = pyqtSignal(str)
    default_signal = pyqtSignal(dict)

    def __init__(self, parent, client):
        super().__init__()
        self.client = client
        self.client.member = self
        self.boss = False
        self.name = ''
        self.room = None
        self.message_signal.connect(parent.refresh_chat)
        self.game_signal.connect(parent.init_game)
        self.custom_signal.connect(parent.show_custom)
        self.player_list_signal.connect(parent.refresh_list)
        self.color_signal.connect(parent.refresh_color)
        self.show_speed_signal.connect(parent.refresh_speed)
        self.show_score_signal.connect(parent.refresh_score)
        self.play_signal.connect(parent.init_countdown)
        self.countdown_signal.connect(parent.countdown)
        self.default_signal.connect(parent.defaults)

    def chat_text(self, event):
        username = event[0]
        text = event[1]
        chat_request = {'status': 'chat', 'data': {
            'user': username, 'text': text, 'room': self.room}}
        self.client.send(chat_request, 'json')

    def try_playing(self, event):
        if event:
            try_request = {'status': 'try_playing', 'data': self.room}
            self.client.send(try_request, 'json')

    def prepare(self, event):
        if event:
            countdown_request = {'status': 'countdown', 'data': self.room}
            self.client.send(countdown_request, 'json')

    def ready(self, event):
        if event:
            play_request = {'status': 'start', 'data': {'room': self.room}}
            self.client.send(play_request, 'pickle')

    def leave_room(self, event):
        if event:
            leave_request = {'status': 'leave', 'data': [self.room, self.boss]}
            self.client.send(leave_request, 'pickle')

    def request_color(self, event):
        color_request = {'status': 'color', 'data': {
            'room': self.room, 'color': self.color, 'new_color': event}}
        self.client.send(color_request, 'json')

    def set_speed(self, event):
        speed_request = {'status': 'speed', 'data': {
            'room': self.room, 'speed': event}}
        self.client.send(speed_request, 'json')

    def set_score(self, event):
        score_request = {'status': 'score', 'data': {
            'room': self.room, 'score': event}}
        self.client.send(score_request, 'json')

    def select_powers(self, event):
        select_powers_request = {'status': 'power', 'data': {
            'power': event[0], 'active': event[1], 'room': self.room}}
        self.client.send(select_powers_request, 'json')

    def check_count(self, event):
        sleep(1)
        if event == '0':
            self.countdown_signal.emit('ready')
        else:
            number = int(event) - 1
            self.countdown_signal.emit(str(number))


# Lógica del Juego
class Player(QObject):

    position_signal = pyqtSignal(dict)
    power_signal = pyqtSignal(dict)
    delete_power_signal = pyqtSignal(int)
    clean_signal = pyqtSignal(bool)
    set_up_signal = pyqtSignal(dict)
    paused_signal = pyqtSignal(bool)
    close_signal = pyqtSignal(bool)
    label_signal = pyqtSignal(bool)

    collisions_list = list()
    opponents_dict = dict()

    def __init__(self,  parent, client):
        super().__init__()
        self.alive = True
        self._x = 0
        self._y = 0
        self._angle = 0
        self.angle_var = 6
        self.direction = 'S'
        self.interval = 40
        self.position_signal.connect(parent.update_position)
        self.power_signal.connect(parent.spawn_power)
        self.delete_power_signal.connect(parent.delete_power)
        self.clean_signal.connect(parent.clean_map)
        self.set_up_signal.connect(parent.set_up)
        self.paused_signal.connect(parent.pause_state)
        self.close_signal.connect(parent.closed)
        self.label_signal.connect(parent.finish)
        self.tick_timer = QTimer()
        self.tick_timer.timeout.connect(self.tick)
        self.trail = True
        self.trail_timer = QTimer()
        self.trail_timer.timeout.connect(self.trail_tick)
        self.trail_remaining = 0
        self.collision = QRect(self.x, self.y, 14, 14)
        self.borders = [QRect(0, 0, 700, - 1), QRect(0, 600, 700, 1),
                        QRect(0, 0, - 1, 600), QRect(700, 0, 1, 600)]
        self.collisions_list = Player.collisions_list
        self.opponents_dict = Player.opponents_dict
        self.safe_trail = deque()
        self.inverted = [False, None]
        self.solid = [True, None]
        self.teleport = [False, None]
        self.tau = 'S'
        self.tau_id = None
        self.color = None
        self.room = 0
        self.client = client
        self.client.player = self
        self.immune = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self.teleport[0]:
            if value >= 700:
                value -= 718
            elif value < 0:
                value += 718
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self.teleport[0]:
            if value >= 600:
                value -= 618
            elif value < 0:
                value += 618
        self._y = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        self._angle = value

    def set_direction(self, event):
        self.direction = event

    def set_tau(self, event):
        if self.angle_var == 90:
            self.tau = event

    def move(self):
        direction = self.direction
        if self.angle_var == 90:
            direction = self.tau
            if self.tau != 'S':
                self.tau = 'S'
        left = 'L'
        right = 'R'
        if self.inverted[0]:
            left = 'R'
            right = 'L'
        if direction == right:
            self.angle -= self.angle_var
        elif direction == left:
            self.angle += self.angle_var
        old_x = self.x
        old_y = self.y
        dx = int(round(3 * m.cos(m.radians(self.angle)), 0))
        dy = int(round(3 * m.sin(m.radians(self.angle)), 0))
        self.x += dx
        self.y -= dy
        self.collision = QRect(self.x, self.y, 14, 14)
        if self.trail and self.solid[0]:
            rect = QRect(old_x + 6, old_y + 6, 2, 2)
            self.collisions_list.append(rect)
            self.safe_trail.append(rect)
        self.position_signal.emit({'x': self.x, 'y': self.y,
                                   'trail_x': old_x + 6,
                                   'trail_y': old_y + 6,
                                   'trail': self.trail and self.solid[0],
                                   'angle': self.angle, 'color': self.color,
                                   'player': True, 'alive': self.alive})

    def trail_tick(self):
        if self.trail_timer.isActive():
            self.trail_timer.stop()
            if self.trail:
                self.trail = False
                self.trail_timer.start(uniform(0, 1) * 1000)
            else:
                self.trail = True
                self.trail_timer.start(uniform(0, 8) * 1000)
        else:
            self.trail_timer.start(uniform(0, 8) * 1000)

    def collide(self):
        collided = False
        crash = False
        if self.solid[0]:
            for player in self.opponents_dict:
                opponent = self.opponents_dict[player]
                if self.collision.intersects(opponent.collision) \
                        and opponent.solid[0]:
                    collided = True
                    crash = player
            for rect in self.collisions_list:
                if self.collision.intersects(rect) and \
                        (rect not in self.safe_trail):
                    collided = True
            for border in self.borders:
                if self.collision.intersects(border) and not self.teleport[0]:
                    collided = True
            if not self.teleport[0]:
                if (self.x >= 700) or (self.x <= 0):
                    collided = True
                if (self.y >= 600) or (self.y <= 0):
                    collided = True
            if len(self.safe_trail) >= 20:
                self.safe_trail.popleft()
        else:
            for border in self.borders:
                if self.collision.intersects(border) and not self.teleport[0]:
                    collided = True
        if collided:
            self.alive = False
            self.send_request(crash)
            self.position_signal.emit({'x': self.x, 'y': self.y,
                                       'trail_x': self.x + 6,
                                       'trail_y': self.y + 6,
                                       'trail': self.trail and self.solid[0],
                                       'angle': self.angle, 'color': self.color,
                                       'player': True, 'alive': self.alive})

    def send_request(self, crash=False):
        request = {'status': 'playing', 'data': {
            'x': self.x, 'y': self.y, 'angle': self.angle,
            'direction': self.direction, 'color': self.color,
            'room': self.room, 'alive': self.alive, 'trail': self.trail,
            'solid': self.solid, 'inverted': self.inverted, 'tau': self.tau,
            'angle_var': self.angle_var, 'teleport': self.teleport,
            'crash': crash}}
        self.client.send(request, 'pickle')

    def start(self, event):
        if event:
            self.tick_timer.start(self.interval)
            self.trail_tick()

    def tick(self):
        if self.alive:
            self.send_request()
        self.move()
        self.collide()
        if not self.alive:
            self.send_request()
            self.tick_timer.stop()
            self.trail_timer.stop()
        self.tick_timer.setInterval(self.interval)

    def set_opponents(self, event):
        self.client.set_opponents(event)

    def set_up(self):
        self.alive = True
        self.angle_var = 6
        self.direction = 'S'
        self.trail = True
        self.trail_remaining = 0
        self.collision = QRect(self.x, self.y, 14, 14)
        Player.collisions_list = list()
        self.collisions_list = Player.collisions_list
        self.safe_trail = deque()
        self.inverted = [False, None]
        self.solid = [True, None]
        self.teleport = [False, None]
        self.tau = 'S'
        self.tau_id = None

    def freeze(self):
        self.immune = True
        self.tick_timer.stop()
        self.trail_timer.stop()

    def pause_server(self, event):
        pause_request = {'status': 'pause', 'data': {
            'paused': event, 'room': self.room}}
        self.client.send(pause_request, 'pickle')

    def pause(self, event):
        if self.alive:
            if event:
                self.direction = 'S'
                self.tick_timer.stop()
                self.trail_remaining = self.trail_timer.remainingTime()
                self.trail_timer.stop()
            else:
                self.tick_timer.start(self.tick_timer.interval())
                self.trail_timer.start(self.trail_remaining)

    def exit(self, event):
        self.alive = False
        self.send_request()
        # stop timers
        exit_response = {'status': 'exit', 'data': {
            'action': event, 'room': self.room}}
        self.client.send(exit_response, 'pickle')


# Lógica de los oponentes
class Opponent(QObject):

    position_signal = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__()
        self.alive = True
        self._x = 0
        self._y = 0
        self._angle = 0
        self.angle_var = 6
        self.direction = 'S'
        self.position_signal.connect(parent.update_position)
        self.trail = True
        self.inverted = [False, None]
        self.collision = QRect(self.x, self.y, 14, 14)
        self.solid = [True, None]
        self.color = None
        self.tau = 'S'
        self.teleport = [False, None]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if self.teleport[0]:
            if value >= 700:
                value -= 718
            elif value < 0:
                value += 718
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self.teleport[0]:
            if value >= 600:
                value -= 618
            elif value < 0:
                value += 618
        self._y = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        self._angle = value

    def move(self):
        direction = self.direction
        if self.angle_var == 90:
            direction = self.tau
            if self.tau != 'S':
                self.tau = 'S'
        left = 'L'
        right = 'R'
        if self.inverted[0]:
            left = 'R'
            right = 'L'
        if direction == right:
            self.angle -= self.angle_var
        elif direction == left:
            self.angle += self.angle_var
        old_x = self.x
        old_y = self.y
        dx = int(round(3 * m.cos(m.radians(self.angle)), 0))
        dy = int(round(3 * m.sin(m.radians(self.angle)), 0))
        self.x += dx
        self.y -= dy
        self.collision = QRect(self.x, self.y, 14, 14)
        if self.trail and self.solid[0]:
            rect = QRect(old_x + 6, old_y + 6, 2, 2)
            Player.collisions_list.append(rect)
        if not self.alive:
            if self.color in Player.opponents_dict:
                del Player.opponents_dict[self.color]
        self.position_signal.emit({'x': self.x, 'y': self.y,
                                   'trail_x': old_x + 6,
                                   'trail_y': old_y + 6,
                                   'trail': self.trail and self.solid[0],
                                   'angle': self.angle, 'color': self.color,
                                   'player': False, 'alive': self.alive})

    def set_up(self, color):
        self.alive = True
        self.angle_var = 6
        self.direction = 'S'
        self.trail = True
        self.inverted = [False, None]
        self.collision = QRect(self.x, self.y, 14, 14)
        self.solid = [True, None]
        self.tau = 'S'
        self.teleport = [False, None]
        self.color = color
        Player.opponents_dict[color] = self
