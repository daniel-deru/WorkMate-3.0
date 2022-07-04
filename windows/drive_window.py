import os
import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.drive_window import Ui_DriveDialog

from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet


class DriveWindow(Ui_DriveDialog, QDialog):
    drive_dict = pyqtSignal(object)
    def __init__(self):
        super(DriveWindow, self).__init__()
        self.setupUi(self)
        self.read_styles()
        
        self.btn_save.clicked.connect(self.save)
        
    def read_styles(self):
        widget_list = [PushButton, CheckBox, Dialog]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
    def save(self):
        drives = {
            'google': self.chk_google.isChecked(),
            'onedrive': self.chk_onedrive.isChecked()
        }
        
        self.drive_dict.emit(drives)
        self.close()
        