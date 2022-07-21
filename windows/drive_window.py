import os
import sys

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QCloseEvent

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.drive_window import Ui_DriveDialog

from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet

from database.model import Model


class DriveWindow(Ui_DriveDialog, QDialog):
    drive_dict = pyqtSignal(object)
    def __init__(self):
        super(DriveWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.read_styles()
        
        self.btn_save.clicked.connect(self.save)
        
        self.data_saved = False
        
    def read_styles(self):
        widget_list = [PushButton, CheckBox, Dialog]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widgets = [
            self.chk_google,
            self.chk_onedrive,
            self.btn_save
        ]
        
        widget: QWidget
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
        
    def save(self):
        drives = {
            'google': self.chk_google.isChecked(),
            'onedrive': self.chk_onedrive.isChecked()
        }
        self.data_saved = True
        self.drive_dict.emit(drives)
        self.close()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.data_saved: self.drive_dict.emit(None)
        return super().closeEvent(event)
        