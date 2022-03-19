#
# pip install pyqt5 keyboard
#

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtCore import QPropertyAnimation, QPoint
import keyboard


class MyNotification(QMainWindow):

    external_key_event = pyqtSignal(object)

    def __init__(self, app):

        QMainWindow.__init__(self)

        # Params...
        self.app = app
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.sw, self.sh = screen_size.width(), screen_size.height()
        self.w, self.h = 500, 200
        print(self.sw, self.sh)

        # < Styles >
        self.background_style_css = "background-color: rgba(0, 0, 0, 150); border-radius: 16px;"
        self.close_button_style_css = """
                                        QPushButton{
                                                    background-color: none;
                                                    color: white; border-radius: 6px;
                                                    font-size: 18px;
                                                    }
                                    """
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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # This Line Set Your Window Always on To
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        # </ Header Style >

        # Keyboard Hook
        self.hook = keyboard.on_press(self.keyboard_on_press_handler)
        self.external_key_event.connect(self.keyboardEventReceived)

        # Initial animation
        self.animation = QPropertyAnimation(self, b'opacity', self)
        self.pulse()

    def keyboard_on_press_handler(self, event):
        self.external_key_event.emit(event)

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

    def close_window(self):
        print("zzzz")
        self.close()
        sys.exit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    MainWindow = MyNotification(app)
    MainWindow.show()
    sys.exit(app.exec_())
