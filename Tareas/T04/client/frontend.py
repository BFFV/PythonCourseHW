import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QTransform, QFont
from PyQt5.QtCore import pyqtSignal, Qt
from backend import Player, Opponent, User, Member
from client import Client


# Aplicación
class DCCurve:

    def __init__(self):
        self.client = Client()
        self.login = LoginWindow(self, self.client)
        self.waiting = WaitingWindow(self, self.client)
        self.play = GameWindow(self, self.client)
        self.login.show()

    def set_keys(self, event):
        self.play.game.left_key = event[0]
        self.play.game.right_key = event[1]

    def enter_room(self):
        self.waiting.set_up()
        if self.waiting.back_member.boss:
            for check in self.waiting.power_checks:
                check.setChecked(True)
            self.waiting.speedSlider.setValue(50)
            self.waiting.scoreBox.setValue(20)
            self.waiting.show_custom()
        else:
            self.waiting.hide_custom()
        self.waiting.show()

    def start_game(self):
        self.play.game.start_playing()


window_name, game_base = uic.loadUiType("windows/LoginWindow.ui")


# Elegir Teclas
class KeySelector(QWidget):

    keys_signal = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)
        self.setGeometry(0, 0, 930, 600)
        self.left_key = None
        self.leftLabel = QLabel(self)
        self.leftLabel.setStyleSheet('color: white')
        self.leftLabel.setFont(QFont('Times', 12))
        self.leftLabel.setText('Haz click aquí y a continuación presiona la '
                               'tecla para girar a la izquierda')
        self.leftLabel.move(200, 400)
        self.right_key = None
        self.rightLabel = QLabel(self)
        self.rightLabel.setStyleSheet('color: white')
        self.rightLabel.setFont(QFont('Times', 12))
        self.rightLabel.setText('Presiona la tecla para girar a la derecha '
                                '(debe ser distinta a la de la izquierda)')
        self.rightLabel.move(200, 400)
        self.keys_signal.connect(parent.ready)
        self.rightLabel.hide()
        self.leftLabel.show()

    def keyPressEvent(self, event):
        if not self.left_key:
            self.left_key = event.key()
            self.leftLabel.hide()
            self.rightLabel.show()
        else:
            if event.key() != self.left_key:
                self.right_key = event.key()
                self.rightLabel.hide()
                self.keys_signal.emit([self.left_key, self.right_key])
                self.left_key = None
                self.right_key = None


# Ventana de Inicio
class LoginWindow(window_name, game_base):

    login_signal = pyqtSignal(list)
    register_signal = pyqtSignal(list)
    assign_signal = pyqtSignal(bool)

    def __init__(self, parent, client):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.setGeometry(150, 100, 930, 600)
        self.client = client
        self.back_user = User(self, self.client)
        self.logButton.clicked.connect(lambda: self.show_inputs('enter'))
        self.signButton.clicked.connect(lambda: self.show_inputs('register'))
        self.backButton.clicked.connect(self.show_options)
        self.registerButton.clicked.connect(lambda: self.send_data('register'))
        self.register_signal.connect(self.back_user.register)
        self.enterButton.clicked.connect(lambda: self.send_data('login'))
        self.login_signal.connect(self.back_user.login)
        self.key_widget = KeySelector(self)
        self.key_widget.hide()
        self.leftLabel.setPixmap(QPixmap('sprites/left.png'))
        self.rightLabel.setPixmap(QPixmap('sprites/right.png'))
        self.leftLabel.hide()
        self.rightLabel.hide()
        self.assign_signal.connect(self.back_user.enter_lobby)
        self.show_options()

    def show_inputs(self, option):
        self.logButton.hide()
        self.signButton.hide()
        self.userLabel.show()
        self.passLabel.show()
        self.userEdit.setText('')
        self.passEdit.setText('')
        self.userEdit.show()
        self.passEdit.show()
        self.backButton.show()
        if option == 'register':
            self.confirmEdit.setText('')
            self.confirmLabel.show()
            self.confirmEdit.show()
            self.registerButton.show()
        else:
            self.enterButton.show()

    def show_options(self):
        self.userLabel.hide()
        self.passLabel.hide()
        self.confirmLabel.hide()
        self.userEdit.hide()
        self.passEdit.hide()
        self.confirmEdit.hide()
        self.registerButton.hide()
        self.enterButton.hide()
        self.backButton.hide()
        self.warningLabel.hide()
        self.logButton.show()
        self.signButton.show()
        self.dccLabel.show()

    def send_data(self, option):
        if (not self.userEdit.text()) or (not self.passEdit.text()):
            self.warningLabel.setText('No se han ingresado todos los datos!')
            self.warningLabel.show()
        elif option == 'register':
            if not self.confirmEdit.text():
                self.warningLabel.setText(
                    'No se han ingresado todos los datos!')
                self.warningLabel.show()
            else:
                self.warningLabel.hide()
                user = self.userEdit.text()
                password = self.passEdit.text()
                confirm = self.confirmEdit.text()
                self.register_signal.emit([user, password, confirm])
        else:
            self.warningLabel.hide()
            user = self.userEdit.text()
            password = self.passEdit.text()
            self.login_signal.emit([user, password])

    def bad_confirmation(self):
        self.warningLabel.setText('La confirmación de la contraseña es '
                                  'distinta!')
        self.warningLabel.show()

    def registered(self, event):
        if event:
            self.show_options()
        else:
            self.warningLabel.setText('El usuario ya existe!')
            self.warningLabel.show()

    def select_keys(self):
        self.userLabel.hide()
        self.passLabel.hide()
        self.userEdit.hide()
        self.passEdit.hide()
        self.enterButton.hide()
        self.backButton.hide()
        self.warningLabel.hide()
        self.dccLabel.hide()
        self.leftLabel.show()
        self.rightLabel.show()
        self.key_widget.leftLabel.show()
        self.key_widget.show()
        self.key_widget.setFocusPolicy(Qt.StrongFocus)

    def login(self, event):
        if event:
            self.select_keys()
        else:
            self.warningLabel.setText('El usuario o la contraseña son '
                                      'incorrectos!')
            self.warningLabel.show()

    def ready(self, event):
        self.leftLabel.hide()
        self.rightLabel.hide()
        self.key_widget.hide()
        self.parent.set_keys(event)
        self.assign_signal.emit(True)

    def assigned(self, event):
        if event:
            self.hide()
            self.parent.enter_room()

    def reset(self):
        self.parent.play.hide()
        self.show_options()
        self.show()


window_name, game_base = uic.loadUiType("windows/WaitingWindow.ui")


# Sala de Espera
class WaitingWindow(window_name, game_base):

    chat_signal = pyqtSignal(list)
    start_game_signal = pyqtSignal(bool)
    leave_signal = pyqtSignal(bool)
    color_signal = pyqtSignal(str)
    speed_signal = pyqtSignal(int)
    score_signal = pyqtSignal(int)
    choose_power_signal = pyqtSignal(list)
    count_signal = pyqtSignal(bool)
    timer_signal = pyqtSignal(str)

    def __init__(self, parent, client):
        super().__init__()
        self.parent = parent
        self.client = client
        self.setupUi(self)
        self.setGeometry(150, 100, 930, 600)
        self.back_member = Member(self, self.client)
        self.playButton.clicked.connect(self.try_start)
        self.start_game_signal.connect(self.back_member.try_playing)
        self.chatButton.clicked.connect(self.send_text)
        self.chat_signal.connect(self.back_member.chat_text)
        self.log = ''
        self.backButton.clicked.connect(self.exit_room)
        self.leave_signal.connect(self.back_member.leave_room)
        self.player_labels = [self.playerLabel_1, self.playerLabel_2,
                              self.playerLabel_3, self.playerLabel_4]
        self.bossLabel.setPixmap(QPixmap('sprites/crown.png'))
        for color in ['Rojo', 'Verde', 'Azul', 'Amarillo']:
            self.colorBox.addItem(color)
        self.colorBox.activated.connect(self.change_color)
        self.color_signal.connect(self.back_member.request_color)
        self.denyLabel.hide()
        self.speedSlider.setMinimum(1)
        self.speedSlider.setMaximum(100)
        self.speedSlider.setValue(50)
        self.speedSlider.valueChanged.connect(self.change_speed)
        self.speed_signal.connect(self.back_member.set_speed)
        self.scoreBox.setValue(20)
        self.scoreBox.setMinimum(1)
        self.scoreBox.setMaximum(100)
        self.scoreBox.valueChanged.connect(self.change_score)
        self.score_signal.connect(self.back_member.set_score)
        self.power_checks = [self.speedCheck, self.cleanCheck,
                             self.solidCheck, self.beerCheck, self.threeCheck,
                             self.coinCheck, self.sleepCheck,
                             self.teleportCheck, self.tauCheck]
        self.speedCheck.stateChanged.connect(
            lambda: self.choose_power(self.speedCheck))
        self.cleanCheck.stateChanged.connect(
            lambda: self.choose_power(self.cleanCheck))
        self.solidCheck.stateChanged.connect(
            lambda: self.choose_power(self.solidCheck))
        self.beerCheck.stateChanged.connect(
            lambda: self.choose_power(self.beerCheck))
        self.threeCheck.stateChanged.connect(
            lambda: self.choose_power(self.threeCheck))
        self.coinCheck.stateChanged.connect(
            lambda: self.choose_power(self.coinCheck))
        self.sleepCheck.stateChanged.connect(
            lambda: self.choose_power(self.sleepCheck))
        self.teleportCheck.stateChanged.connect(
            lambda: self.choose_power(self.teleportCheck))
        self.tauCheck.stateChanged.connect(
            lambda: self.choose_power(self.tauCheck))
        self.choose_power_signal.connect(self.back_member.select_powers)
        self.denyStartLabel.hide()
        self.speedLabel.setText('50')
        self.scoreLabel.setText('20')
        self.count_signal.connect(self.back_member.prepare)
        self.timer_signal.connect(self.back_member.check_count)
        self.countTimer.hide()

    def send_text(self):
        if len(self.chatEdit.text()) != 0:
            message = self.chatEdit.text()
            self.chatEdit.setText('')
            self.chat_signal.emit([self.back_member.name, message])

    def refresh_list(self, event):
        self.denyStartLabel.hide()
        for label in self.player_labels:
            label.setText('')
            label.setStyleSheet(f'background-color: black')
        for label, data in zip(self.player_labels, event):
            label.setText(data[0])
            label.setStyleSheet(f'background-color: {data[1]}')

    def refresh_chat(self, event):
        self.log += event
        self.chatWindow.setText(self.log)

    def change_color(self, event):
        colors = ['red', 'green', 'blue', 'yellow']
        color = colors[event]
        self.color_signal.emit(color)

    def refresh_color(self, event):
        if event:
            self.denyLabel.hide()
        else:
            self.denyLabel.show()

    def change_speed(self, event):
        self.speed_signal.emit(event)

    def refresh_speed(self, event):
        self.speedLabel.setText(event)

    def change_score(self, event):
        self.score_signal.emit(event)

    def refresh_score(self, event):
        self.scoreLabel.setText(event)

    def choose_power(self, event):
        powers = ['speed', 'clean', 'collide', 'beer', 'three',
                  'nebcoin', 'sleep', 'teleport', 'tau']
        index = self.power_checks.index(event)
        chosen = powers[index]
        self.choose_power_signal.emit([chosen, event.isChecked()])

    def try_start(self):
        self.start_game_signal.emit(True)

    def init_countdown(self, event):
        if event:
            self.count_signal.emit(True)
        else:
            self.denyStartLabel.show()

    def countdown(self, event):
        if not event:
            self.hide_custom()
            self.chatButton.hide()
            self.chatEdit.hide()
            self.chatWindow.hide()
            self.backButton.hide()
            self.colorBox.hide()
            self.countTimer.setText('10')
            self.countTimer.show()
            self.timer_signal.emit('10')
        elif event == 'ready':
            self.countTimer.hide()
            self.hide()
            self.parent.play.show()
        else:
            self.countTimer.setText(event)
            self.timer_signal.emit(event)

    def init_game(self, event):
        if event:
            self.parent.start_game()

    def exit_room(self):
        self.leave_signal.emit(True)
        self.hide()
        self.parent.login.show_options()
        self.parent.login.show()

    def set_up(self):
        self.colorBox.setCurrentIndex(
            ['red', 'green', 'blue', 'yellow'].index(self.back_member.color))
        self.colorBox.show()
        self.backButton.show()
        self.chatWindow.show()
        self.chatButton.show()
        self.chatEdit.show()

    def hide_custom(self):
        self.denyStartLabel.hide()
        for check in self.power_checks:
            check.hide()
        self.playButton.hide()
        self.speedSlider.hide()
        self.scoreBox.hide()

    def show_custom(self):
        self.denyStartLabel.hide()
        for check in self.power_checks:
            check.show()
        self.playButton.show()
        self.speedSlider.show()
        self.scoreBox.show()

    def defaults(self, event):
        self.scoreLabel.setText(str(event['score']))
        self.speedLabel.setText(str(event['speed']))


window_name, game_base = uic.loadUiType("windows/GameWindow.ui")


# Sala de Juego
class GameWindow(window_name, game_base):

    pause_signal = pyqtSignal(bool)
    exit_signal = pyqtSignal(str)

    def __init__(self, parent, client):
        super().__init__()
        self.parent = parent
        self.client = client
        self.setupUi(self)
        self.setGeometry(150, 100, 930, 600)
        self.game = MainGame(self, self.client)
        self.game.setFocusPolicy(Qt.StrongFocus)
        self.pause_signal.connect(self.game.back_player.pause_server)
        self.pauseButton.clicked.connect(self.pause_game)
        self.exitButton.clicked.connect(lambda: self.exit_game('exit'))
        self.newButton.clicked.connect(lambda: self.exit_game('new'))
        self.exit_signal.connect(self.game.back_player.exit)
        self.winLabel.hide()
        self.loseLabel.hide()

    def pause_game(self):
        if not self.game.paused:
            self.game.paused = True
        else:
            self.game.paused = False
        self.pause_signal.emit(self.game.paused)

    def exit_game(self, option):
        self.exit_signal.emit(option)


# Juego
class MainGame(QWidget):

    move_signal = pyqtSignal(str)
    start_signal = pyqtSignal(bool)
    tau_signal = pyqtSignal(str)
    set_opponents_signal = pyqtSignal(list)
    play_signal = pyqtSignal(bool)
    freeze_signal = pyqtSignal(bool)

    def __init__(self, parent, client):
        super().__init__(parent)
        self.setGeometry(0, 0, 700, 600)
        self.parent = parent
        self.map = QPixmap('sprites/background.png')
        self.back_player = Player(self, client)
        self.player_map = QPixmap()
        self.front_player = QLabel(self)
        self.front_player.setPixmap(self.player_map)
        self.front_player.setAlignment(Qt.AlignCenter)
        self.move_signal.connect(self.back_player.set_direction)
        self.tau_signal.connect(self.back_player.set_tau)
        self.set_opponents_signal.connect(self.back_player.set_opponents)
        self.play_signal.connect(parent.parent.waiting.back_member.ready)
        self.freeze_signal.connect(self.back_player.pause)
        self.opponents_dict = dict()
        self.opponents = list()
        for opponent in range(3):
            back_opponent = Opponent(self)
            self.opponents.append(back_opponent)
        self.set_opponents_signal.emit(self.opponents)
        self.powers = list()
        self.paused = False
        self.start_signal.connect(self.back_player.start)
        self.left_key = None
        self.right_key = None

    def keyPressEvent(self, event):
        if event.key() == self.right_key:
            if not event.isAutoRepeat():
                self.tau_signal.emit('R')
            self.move_signal.emit('R')
        elif event.key() == self.left_key:
            if not event.isAutoRepeat():
                self.tau_signal.emit('L')
            self.move_signal.emit('L')
        elif event.key() == Qt.Key_Space:
            self.play_signal.emit(True)

    def keyReleaseEvent(self, event):
        if event.key() == self.right_key:
            self.move_signal.emit('S')
        elif event.key() == self.left_key:
            self.move_signal.emit('S')

    def traces(self, event):
        color_dict = {'red': Qt.red, 'blue': Qt.blue, 'green': Qt.green,
                      'yellow': Qt.yellow}
        color = color_dict[event['color']]
        qp = QPainter(self.map)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QPen(color, 0, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin))
        qp.setBrush(QBrush(color))
        qp.drawEllipse(event['trail_x'], event['trail_y'], 5, 5)
        qp.end()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.map)

    @staticmethod
    def rotate(angle, entity, sprite):
        entity.setPixmap(sprite.transformed(QTransform().rotate(- angle)))

    def start_playing(self):
        self.start_signal.emit(True)

    def update_position(self, event):
        entity = self.front_player
        sprite = self.player_map
        if not event['player']:
            entity = self.opponents_dict[event['color']][0]
            sprite = self.opponents_dict[event['color']][1]
        self.rotate(event['angle'], entity, sprite)
        entity.move(event['x'], event['y'])
        if not event['alive']:
            entity.setPixmap(QPixmap())
        elif event['trail']:
            self.traces(event)

    def spawn_power(self, event):
        power_label = QLabel(self)
        name = event['name']
        power_label.setPixmap(QPixmap(f'sprites/{name}.png'))
        power_label.move(event['x'], event['y'])
        power_label.show()
        self.powers.append([event['id'], power_label])

    def delete_power(self, event):
        for power in self.powers:
            if power[0] == event:
                power[1].hide()
                self.powers.remove(power)

    def clean_map(self, event):
        if event:
            self.map = QPixmap('sprites/background.png')
            self.update()

    def set_up(self, event):
        self.parent.winLabel.hide()
        self.parent.loseLabel.hide()
        self.paused = False
        self.clean_map(True)
        for color in event:
            if color == self.back_player.color:
                player = event[color]
                self.player_map = QPixmap(f'sprites/{color}.png')
                self.front_player.move(player[0], player[1])
                self.rotate(player[2], self.front_player, self.player_map)
            else:
                for opponent in self.opponents_dict.values():
                    opponent[0].hide()
                opponent = event[color]
                front_opponent = QLabel(self)
                opponent_map = QPixmap(f'sprites/{color}.png')
                front_opponent.setPixmap(opponent_map)
                front_opponent.setAlignment(Qt.AlignCenter)
                self.opponents_dict[color] = [front_opponent, opponent_map]
                front_opponent.move(opponent[0], opponent[1])
                front_opponent.show()
                self.rotate(opponent[2], front_opponent, opponent_map)

    def pause_state(self, event):
        self.paused = event
        self.freeze_signal.emit(event)

    def closed(self):
        self.hide()

    def finish(self, event):
        if event:
            self.parent.winLabel.show()
        else:
            self.parent.loseLabel.show()


if __name__ == '__main__':
    app = QApplication([])
    main_app = DCCurve()
    sys.exit(app.exec_())
