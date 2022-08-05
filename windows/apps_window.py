import sys
import os
from PyQt5.QtWidgets import QDialog, QFileDialog, QListView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.app_window import Ui_App_Window
from database.model import Model
from utils.message import Message
from utils.helpers import StyleSheet, set_font

import assets.resources

from widgetStyles.Dialog import Dialog
from widgetStyles.LineEdit import LineEdit
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.SpinBox import SpinBox
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class Apps_window(Ui_App_Window, QDialog):
    app_window_signal = pyqtSignal(str)
    def __init__(self, app=None):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.show_groups()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowTitle("Add Your App")
        self.read_styles()
        self.apps = Model().read('apps')

        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        self.btn_discard.clicked.connect(lambda: self.close())
        
    def show_groups(self):
        groups = Model().read("groups")
        for group in groups:
            self.cmb_group.addItem(group[1], group[0])
        

    def save_clicked(self):
        
        name = self.lnedt_name.text()
        path = self.lnedt_path.text()
        group = self.cmb_group.currentData()

        data = {
                    'name': name,
                    'path': path,
                    'sequence': '0',
                    'group_id': group
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
            Model().save('apps', data)
            self.app_window_signal.emit("saved")
        self.close()

    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)

    def read_styles(self):
        self.cmb_group.setView(QListView())
        self.cmb_group.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        
        styles = [
            Dialog,
            LineEdit,
            PushButton,
            Label,
            SpinBox,
            SettingsCheckBox,
            ComboBox
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.btn_save,
            self.btn_desktop,
            self.btn_discard,
            self.lbl_name,
            self.lbl_path,
            self.lnedt_name,
            self.lnedt_path,
            self.lbl_group,
            self.cmb_group,
            self.cmb_group.view()
        ]
        
        set_font(font_list)