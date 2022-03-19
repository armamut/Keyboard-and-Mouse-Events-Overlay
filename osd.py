#
# pip install pyqt5 keyboard mouse
#

import sys
from PyQt5.QtCore import pyqtSlot, pyqtProperty
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtCore import QPropertyAnimation, QPoint
import keyboard
import mouse
from numpy import isin


class MouseOverlay(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.radius = 50
        # < Styles >
        self.background_style_css = f"background-color: rgba(255, 255, 50, 255); border-radius: {self.radius}px;"
        self.setFixedSize(self.radius * 2, self.radius * 2)
        self.move(100, 100)
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.main_back = QLabel(self)
        self.main_back.resize(self.radius * 2, self.radius * 2)
        self.main_back.setStyleSheet(self.background_style_css)
        self.setWindowOpacity(0.25)

        self.animation = QPropertyAnimation(self, b'opacity', self)

    # Opacity Property =======
    def windowOpacity(self):
        return super().windowOpacity()

    def setWindowOpacity(self, opacity):
        super().setWindowOpacity(opacity)

    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)

    def pulse(self):
        self.animation.stop()
        self.animation.setDuration(400)
        self.animation.setLoopCount(1)
        self.animation.setStartValue(0.8)
        self.animation.setEndValue(0.25)
        self.animation.start(QPropertyAnimation.KeepWhenStopped)


class KeyboardOverlay(QMainWindow):

    external_key_event = pyqtSignal(object)
    external_mouse_event = pyqtSignal(object)

    def __init__(self, app):

        QMainWindow.__init__(self)

        # Find screen size
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.sw, self.sh = screen_size.width(), screen_size.height()
        self.w, self.h = 500, 200
        print(self.sw, self.sh)

        # < Styles >
        self.background_style_css = "background-color: rgba(0, 0, 0, 150); border-radius: 16px;"
        # </ Styles >

        # < Global Settings >
        self.setFixedSize(self.w, self.h)
        self.move((self.sw - self.w) // 2, self.sh - self.h - 70)
        # </ Global Settings >

        # < Main Style >
        self.main_back = QLabel(self)
        self.main_back.resize(500, 200)
        self.main_back.setStyleSheet(self.background_style_css)
        # </ Main Style >

        # < Text Label >
        self.text_label = QLabel(self)
        self.text_label.move(10, 5)
        self.text_label.resize(480, 190)
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setText("Keyboard Display is ON")
        self.text_label.setStyleSheet("color: white; font-size: 24pt;")
        # < Text Label >

        # creating a QGraphicsDropShadowEffect object
        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(0, 0, 0, 250))
        shadow.setOffset(0)
        shadow.setBlurRadius(15)
        self.text_label.setGraphicsEffect(shadow)

        # < Header Style >
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowTransparentForInput)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # </ Header Style >

        # Keyboard Hook
        self.keyboard_hook = keyboard.on_press(self.keyboard_on_press_handler)
        self.external_key_event.connect(self.keyboardEventReceived)
        self.mouse_hook = mouse.hook(self.mouse_event_handler)
        self.external_mouse_event.connect(self.mouseEventReceived)

        # Initial animation
        self.animation = QPropertyAnimation(self, b'opacity', self)
        self.pulse()

        self.mc = MouseOverlay()
        self.mc.show()


    # Keyboard handler
    def keyboard_on_press_handler(self, event):
        self.external_key_event.emit(event)

    # Mouse handler
    def mouse_event_handler(self, event):
        self.external_mouse_event.emit(event)

    @pyqtSlot(object)
    def mouseEventReceived(self, event):
        # print(event)
        if isinstance(event, mouse.MoveEvent):
            self.mc.move(event.x - self.mc.radius, event.y - self.mc.radius)
        if isinstance(event, mouse.ButtonEvent) and event.event_type != 'up':
            self.mc.pulse()


    @pyqtSlot(object)
    def keyboardEventReceived(self, event):
        txt = []
        if keyboard.is_pressed('ctrl'):
            txt.append('[CTRL]')
        if keyboard.is_pressed('shift'):
            txt.append('[SHIFT]')
        if keyboard.is_pressed('alt'):
            txt.append('[ALT]')
        if keyboard.is_pressed('alt gr'):
            txt.append('[ALT GR]')
        if keyboard.is_pressed('windows'):
            txt.append('[WIN]')
        if event.name not in ['ctrl', 'shift', 'alt', 'alt gr', 'right ctrl', 'right shift', 'left windows']:
            tr_upper = str.maketrans("ğüşiöçı", "ĞÜŞİÖÇI")
            t = (event.name
                 .replace('print screen', 'PRINTSCREEN')
                 .replace('page up', 'PAGE UP')
                 .replace('page down', 'PAGE DOWN')
                 .replace('left windows', 'WIN')
                 .replace('decimal', ',')
                 .replace('backspace', '⌫')
                 .replace('left', '🡄')
                 .replace('right', '🡆')
                 .replace('up', '🡅')
                 .replace('down', '🡇')
                 )
            if len(t) > 1:
                t = f'[{t.upper()}]'
            else:
                t = t.translate(tr_upper).upper()
            txt.append(t)
        txt = " + ".join(txt)
        self.text_label.setText(txt)
        self.pulse()

    def pulse(self):
        self.animation.stop()
        self.animation.setDuration(2000)
        self.animation.setLoopCount(1)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start(QPropertyAnimation.KeepWhenStopped)

    # Opacity Property =======

    def windowOpacity(self):
        return super().windowOpacity()

    def setWindowOpacity(self, opacity):
        super().setWindowOpacity(opacity)

    opacity = pyqtProperty(float, windowOpacity, setWindowOpacity)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = KeyboardOverlay(app)
    MainWindow.show()
    sys.exit(app.exec_())
