import sys
import os
from functools import reduce
import re

from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

from utils.helpers import clear_window

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Widget import Widget
from utils.helpers import StyleSheet

from database.model import Model


class SettingsTab(QWidget, Ui_Settings_tab):
    settings_signal = pyqtSignal(str)
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        settings = Model().read('settings')[0]
        nightmode = settings[1]
        self.chkbx_night_mode.setChecked(nightmode)

        self.chkbx_night_mode.stateChanged.connect(self.set_night_mode)
        self.btn_color.clicked.connect(self.set_color)
        self.fcmbx_font.currentFontChanged.connect(self.set_font)
        self.btn_reset.clicked.connect(self.reset)
        self.settings_signal.connect(self.read_styles)
    
    def create_tab(self):
        return self

    def set_night_mode(self):
        nightmode = self.chkbx_night_mode.isChecked()
        Model().update("settings", {'nightmode': nightmode}, 'settings')
        self.settings_signal.emit("settings changed")
        self.updateWindow()

    def set_font(self):
        font = self.fcmbx_font.currentFont().family()
        Model().update("settings", {'font': font}, 'settings')
        self.settings_signal.emit("settings changed")
        

    def set_color(self):
        color = QColorDialog().getColor().name()
        Model().update("settings", {'color': color}, 'settings')
        self.settings_signal.emit("settings changed")

    def reset(self):
        Model().reset()
        self.settings_signal.emit("settings changed")
    
    def updateWindow(self):
        self.read_styles()
        self.settings_signal.emit("settings")

    def read_styles(self):
        styles = [Label, PushButton, CheckBox]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.lbl_color.setFont(QFont(font))
        self.lbl_night_mode.setFont(QFont(font))
        self.lbl_font.setFont(QFont(font))
        self.btn_color.setFont(QFont(font))
        self.btn_export_apps.setFont(QFont(font))
        self.btn_export_notes.setFont(QFont(font))
        self.btn_import_apps.setFont(QFont(font))
        self.btn_import_notes.setFont(QFont(font))
        self.btn_reset.setFont(QFont(font))
