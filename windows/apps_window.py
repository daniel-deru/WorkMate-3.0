import sys
import os
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_window import Ui_App_Window
from database.model import Model
from utils.message import Message
from utils.helpers import StyleSheet

import assets.resources

from widgetStyles.Dialog import Dialog
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox
from widgetStyles.QCheckBox import SettingsCheckBox

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class Apps_window(QDialog, Ui_App_Window):
    app_window_signal = pyqtSignal(str)
    def __init__(self, app=None):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowTitle("Add Your App")
        self.read_styles()
        self.apps = Model().read('apps')
        self.spn_index.setValue(len(self.apps) + 1)
        self.spn_index.setMaximum(len(self.apps) + 1)
        self.spn_index.setMinimum(1)

        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        self.btn_discard.clicked.connect(lambda: self.close())

    def save_clicked(self):
        
        name = self.lnedt_name.text()
        index = self.spn_index.value()
        path = self.lnedt_path.text()

        data = {
                    'name': name,
                    'path': path,
                    'sequence': index,
                }

        if not name:
            Message("Please enter a name for your app", "No name").exec_()
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
        else:
            self.save_apps(data)
    
    def save_apps(self, data):
        is_unique = True
        for app in self.apps:
            if data['name'] in app:
                Message("This name is already being used", "Name already exists").exec_()
                is_unique = False

            elif data['path'] in app:
                Message("This path is already being used", "Path already exists").exec_()
                is_unique = False
        if is_unique:
            for app in self.apps:

                if data['sequence'] <= len(self.apps):

                    if app[3] >= data['sequence']:
                        Model().update('apps', {'sequence': app[3] + 1}, app[0])
            Model().save('apps', data)
            self.app_window_signal.emit("saved")
        self.close()

    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)

    def read_styles(self):
        styles = [
            Dialog,
            LineEdit,
            PushButton,
            Label,
            SpinBox,
            SettingsCheckBox
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.btn_save.setFont(QFont(font))
        self.btn_desktop.setFont(QFont(font))
        self.btn_discard.setFont(QFont(font))
        self.lbl_name.setFont(QFont(font))
        self.lbl_index.setFont(QFont(font))
        self.lbl_path.setFont(QFont(font))
        self.lnedt_name.setFont(QFont(font))
        self.lnedt_path.setFont(QFont(font))
        self.spn_index.setFont(QFont(font))