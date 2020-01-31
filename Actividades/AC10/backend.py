# Acá va lo relacionado con el procesamiento de datos
from PyQt5.QtCore import QObject, pyqtSignal, QRect
from PyQt5.Qt import QTest


class Valid(QObject):

    check_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.check_signal.connect(parent.open_window)

    def check(self, user):
        if user.isalpha() and (len(user) > 6):
            self.check_signal.emit(True)
        else:
            self.check_signal.emit(False)


class Character(QObject):

    update_position_signal = pyqtSignal(dict)

    def __init__(self,  parent, x, y):
        super().__init__()
        self.direction = 'R'
        self._x = x
        self._y = y
        self.update_position_signal.connect(parent.update_position)
        self.cherries = []

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if 8 < value < 590:
            self._y = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 10 < value < 530:
            self._x = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    def move(self, event):
        if event == 'R':
            self.x += 10
            self.direction = 'R'
        if event == 'L':
            self.x -= 10
            self.direction = 'L'
        if event == 'U':
            self.y -= 10
            self.direction = 'U'
        if event == 'D':
            self.y += 10
            self.direction = 'D'
