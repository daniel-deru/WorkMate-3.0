import sys
import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtCore import QLine, pyqtSignal, Qt
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
from widgetStyles.QCheckBox import CheckBox, SettingsCheckBox




DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class Apps_window(QDialog, Ui_App_Window):
    app_window_signal = pyqtSignal(str)
    def __init__(self, app=None):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon("./assets/WorkMate.ico"))
        self.setWindowTitle("Add Your App")
        self.read_styles()
        self.apps = Model().read('apps')
        self.protected_apps = Model().read("protected_apps")
        self.spn_index.setValue(len(self.apps) + 1)
        self.spn_index.setMaximum(len(self.apps) + 1)
        self.spn_index.setMinimum(1)

        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        self.chkbox_protected_app.stateChanged.connect(self.protected_toggle)
        

        # self.app = app
        # if self.app is not None: 
        #     self.setWindowTitle("Update Your App")    
        #     self.btn_save.setText("Update")
        #     self.lnedt_name.setText(self.app[1])
        #     self.lnedt_path.setText(self.app[2])
        #     self.spn_index.setValue(self.app[3])


    def save_clicked(self):
        
        name = self.lnedt_name.text()
        index = self.spn_index.value()
        path = self.lnedt_path.text()

        data = {
                    'name': name,
                    'path': path,
                    'sequence': index,
                }
            
        if self.chkbox_protected_app.isChecked():
            username = self.lnedt_username.text()
            email = self.lnedt_email.text()
            password = self.lnedt_password.text()
            if not password:
                Message("Please enter the password used by the protected app", "Password Required").exec_()
                return
            elif not username and not email:
                Message("You must provide either a username or an email that is used by the protected app", "Missing field").exec_()
                return
            else:
                data["username"] = username
                data["email"] = email
                data["password"] = password

        if not name:
            Message("Please enter a name for your app", "No name").exec_()
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
        else:
            if self.chkbox_protected_app.isChecked():
                self.save_protected_apps(data)
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
        if is_unique and not self.app:
            for app in self.apps:

                if data['sequence'] <= len(self.apps):

                    if app[3] >= data['sequence']:
                        Model().update('apps', {'sequence': app[3] + 1}, app[0])
            Model().save('apps', data)
            self.app_window_signal.emit("saved")
        self.close()

    def save_protected_apps(self, data):
        is_unique = True
        for app in self.protected_apps:
            if data['name'] in app and self.app is None:
                Message("This name is already being used", "Name already exists").exec_()
                is_unique = False

            elif data['path'] in app and self.app is None:
                Message("This path is already being used", "Path already exists").exec_()
                is_unique = False
        if is_unique and not self.app:
            for app in self.protected_apps:

                if data['sequence'] <= len(self.protected_apps):

                    if app[3] >= data['sequence']:
                        Model().update('protected_apps', {'sequence': app[3] + 1}, app[0])
            Model().save('protected_apps', data)
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

    
    def protected_toggle(self):
        toggle = self.chkbox_protected_app
        if toggle.isChecked():
            self.add_protected_fields()
            self.spn_index.setValue(len(self.protected_apps) + 1)
            self.spn_index.setMaximum(len(self.protected_apps) + 1)
            self.spn_index.setMinimum(1)
        elif not toggle.isChecked():
            self.remove_protected_fields()
            self.spn_index.setValue(len(self.apps) + 1)
            self.spn_index.setMaximum(len(self.apps) + 1)
            self.spn_index.setMinimum(1)
        
    def add_protected_fields(self):
        font = Model().read('settings')[0][2]

        self.lbl_username = QLabel("Username")
        self.lbl_email = QLabel("Email")
        self.lbl_password = QLabel("Password")

        self.lnedt_username = QLineEdit()
        self.lnedt_email = QLineEdit()
        self.lnedt_password = QLineEdit()

        self.vbox_username = QVBoxLayout()
        self.vbox_email = QVBoxLayout()
        self.vbox_password = QVBoxLayout()

        self.vbox_username.addWidget(self.lbl_username)
        self.vbox_username.addWidget(self.lnedt_username)

        self.vbox_email.addWidget(self.lbl_email)
        self.vbox_email.addWidget(self.lnedt_email)

        self.vbox_password.addWidget(self.lbl_password)
        self.vbox_password.addWidget(self.lnedt_password)

        self.vbox_protected_fields.addLayout(self.vbox_username)
        self.vbox_protected_fields.addLayout(self.vbox_email)
        self.vbox_protected_fields.addLayout(self.vbox_password)

        self.lbl_username.setFont(QFont(font))
        self.lbl_password.setFont(QFont(font))
        self.lbl_email.setFont(QFont(font))

        self.lnedt_username.setFont(QFont(font))
        self.lnedt_password.setFont(QFont(font))
        self.lnedt_email.setFont(QFont(font))


    def remove_protected_fields(self):

        self.lbl_password.deleteLater()
        self.lbl_username.deleteLater()
        self.lbl_email.deleteLater()

        self.lnedt_password.deleteLater()
        self.lnedt_email.deleteLater()
        self.lnedt_username.deleteLater()

        self.vbox_password.deleteLater()
        self.vbox_email.deleteLater()
        self.vbox_username.deleteLater()



        


            
