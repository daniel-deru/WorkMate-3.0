import sys
import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QAbstractSpinBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_window import Ui_App_Window
from database.model import Model
from utils.message import Message
from utils.helpers import StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox

from tabs.vault_tab import Vault_tab



DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class Apps_window(QDialog, Ui_App_Window):
    app_window_signal = pyqtSignal(str)
    def __init__(self, app=None):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon("./assets/WorkMate.ico"))
        self.read_styles()
        self.apps = Model().read('apps')
        self.spn_index.setValue(len(self.apps) + 1)
        self.spn_index.setMaximum(len(self.apps) + 1)
        self.spn_index.setMinimum(1)

        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        

        self.app = app
        if self.app is not None:     
            self.btn_save.setText("Update")
            self.lnedt_name.setText(self.app[1])
            self.lnedt_path.setText(self.app[2])
            self.spn_index.setValue(self.app[3])

    def save_clicked(self):
        
        name = self.lnedt_name.text()
        index = self.spn_index.value()
        path = self.lnedt_path.text()
        username = self.lnedt_username.text()
        password = self.lnedt_password.text()
        data = {
                    'name': name,
                    'path': path,
                    'sequence': index,
                    'username': username,
                    'password': password
                }

        is_unique = True
        if not name:
            Message("Please enter a name for your app", "No name").exec_()
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
        else:
            for app in self.apps:

                if name in app and self.app is None:
                    Message("This name is already being used", "Name already exists").exec_()
                    is_unique = False

                elif path in app and self.app is None:
                    Message("This path is already being used", "Path already exists").exec_()
                    is_unique = False

            if is_unique and not self.app:
                for app in self.apps:

                    if index <= len(self.apps):

                        if app[3] >= index:
                            Model().update('apps', {'sequence': app[3] + 1}, app[0])
                Model().save('apps', data)
                self.app_window_signal.emit("saved")
                self.close()

            elif self.app is not None:
                if self.app[3] != index:
                    old = self.app[3] - 1
                    new = index - 1
                    move_up = True if old > new else False
                    global array
                    if move_up:
                        array = self.apps[new:old]
                    elif not move_up:
                        array = self.apps[old+1:new+1]
                    for app in array:
                        app = list(app)
                        if move_up:
                            Model().update('apps', {'sequence': app[3] + 1}, app[0])
                        elif not move_up:
                            Model().update('apps', {'sequence': app[3] - 1}, app[0])
                Model().update('apps', data, self.app[0])
                self.app_window_signal.emit("updated")
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
        self.lbl_username.setFont(QFont(font))
        self.lbl_password.setFont(QFont(font))
        self.lnedt_username.setFont(QFont(font))
        self.lnedt_password.setFont(QFont(font))
