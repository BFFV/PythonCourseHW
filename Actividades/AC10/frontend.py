# Acá va lo relacionado con la GUI.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, \
    QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from backend import Valid, Character
from random import randint


class MainWindow(QWidget):

    check_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Pac-Man')
        self.label = QLabel('Ingrese su usuario:', self)
        self.label.move(100, 85)
        self.warning = QLabel('', self)
        self.warning.setFixedSize(120, 10)
        self.warning.move(90, 160)
        self.username = QLineEdit('', self)
        self.username.setGeometry(100, 100, 100, 20)
        self.start = QPushButton('&Inicio', self)
        self.start.resize(self.start.sizeHint())
        self.start.move(110, 130)
        self.start.clicked.connect(self.check)
        self.validation = Valid(self)
        self.check_signal.connect(self.validation.check)
        self.show()

    def check(self):
        self.check_signal.emit(self.username.text())

    def open_window(self, state):
        if state:
            self.hide()
            self.maingame = MainGame()
            self.maingame.show()
        else:
            self.warning.setText('El usuario no es válido!!!')


class MainGame(QWidget):

    move_character_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 560, 610)
        self.setWindowTitle('Pac-Man')
        self._frame = 1
        self.background = QLabel(self)
        self.background.setPixmap(QPixmap('sprites/map.png'))
        self.backend_character = Character(self, 20, 20)
        self.move_character_signal.connect(self.backend_character.move)
        self.front_character = QLabel(self)
        self.front_character.setPixmap(QPixmap('sprites/pacman_R_2.png'))
        self.front_character.move(20, 20)

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def keyPressEvent(self, e):
        self.frame += 1
        if e.key() == Qt.Key_Right:
            self.front_character.setPixmap(QPixmap(f'sprites/pacman_R_{self.frame}.png'))
            self.move_character_signal.emit('R')
        if e.key() == Qt.Key_Left:
            self.front_character.setPixmap(QPixmap(f'sprites/pacman_L_{self.frame}.png'))
            self.move_character_signal.emit('L')
        if e.key() == Qt.Key_Up:
            self.front_character.setPixmap(QPixmap(f'sprites/pacman_U_{self.frame}.png'))
            self.move_character_signal.emit('U')
        if e.key() == Qt.Key_Down:
            self.front_character.setPixmap(QPixmap(f'sprites/pacman_D_{self.frame}.png'))
            self.move_character_signal.emit('D')
        if e.key() == Qt.Key_Space:
            x = randint(11, 529)
            y = randint(9, 589)
            self.cherry = QLabel(self)
            self.cherry.setPixmap(QPixmap('sprites/cherry.png'))
            self.cherry.move(x, y)
            self.cherry.show()
            self.backend_character.cherries.append(self.cherry)

    def update_position(self, event):
        self.front_character.move(event['x'], event['y'])


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
