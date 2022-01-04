import os
import sys

from PyQt5.QtWidgets import QDialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.timer_window import Ui_Timer
from utils.helpers import StyleSheet
from database.model import Model

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog

class Timer(Ui_Timer, QDialog):
    def __init__(self):
        super(Timer, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.hslide_timer.valueChanged.connect(self.slider)
        self.btn_save.clicked.connect(self.save)
    
    def slider(self):
        self.lcd_timer.display(self.hslide_timer.value())

    def read_styles(self):
        styles = [
            Dialog,
            PushButton,
            Label
            ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def save(self):
        Model().update("settings", {"timer": self.hslide_timer.value()}, 'settings')
        self.close()