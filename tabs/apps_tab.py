import sys
import os
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.apps_tab import Ui_apps_tab
from database.model import Model

from windows.apps_window import Apps_window
from windows.apps_edit_window import AppsEdit

from widgets.app_item import AppItem
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBoxSquare
from widgetStyles.Line import Line
from widgetStyles.Label import Label

from utils.helpers import StyleSheet
from utils.helpers import clear_window

class Apps_tab(Ui_apps_tab, QWidget):
    app_signal = pyqtSignal(str)
    table_signal = pyqtSignal(str)
    # This signal is to communicate with the main window where the login will take place
    login_signal = pyqtSignal(str)

    def __init__(self):
        super(Apps_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.create_apps()
        # self.create_protected_apps()

        self.btn_add_app.clicked.connect(self.add_app)
        self.chk_edit_apps.stateChanged.connect(self.edit_checked)
        self.chk_delete_apps.stateChanged.connect(self.delete_checked)

        self.logged_in = False
        
        # Signal slots for external signals
        self.app_signal.connect(self.update)
        # Login signal will run everytime the login signal is updated
    
    def create_tab(self):
        return self

    def read_styles(self):
        styles = [CheckBoxSquare, PushButton, Line, Label]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        widgetList = [
            self.btn_add_app,
            self.chk_edit_apps,
            self.chk_delete_apps,
            self.lbl_open_apps,
        ]
        font = Model().read('settings')[0][2]

        for i in range(len(widgetList)):
            widgetList[i].setFont(QFont(font))

        # self.line.setStyleSheet("border: 2px solid green;")

    def add_app(self):
        app_window = Apps_window()
        app_window.app_window_signal.connect(self.update)
        app_window.exec_()
    
    def create_apps(self):
        apps = Model().read('apps')
        COLUMNS = 4
        sorted_apps = sorted(apps, key=lambda item: item[2])
        grid_items = []
        for i in range(math.ceil(len(sorted_apps)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if sorted_apps:
                    subarr.append(sorted_apps.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                app_button = AppItem(grid_items[i][j]).create()
                app_button.app_clicked_signal.connect(self.get_app)
                self.gbox_apps.addWidget(app_button, row, col)

    def edit_checked(self):
        delete_apps = self.chk_delete_apps
        edit_apps = self.chk_edit_apps

        if delete_apps.isChecked() and edit_apps.isChecked():
            edit_apps.setChecked(True)
            delete_apps.setChecked(False)
          
    def delete_checked(self):
        delete_apps = self.chk_delete_apps
        edit_apps = self.chk_edit_apps

        if edit_apps.isChecked() and delete_apps.isChecked():
            delete_apps.setChecked(True)
            edit_apps.setChecked(False)
    
    def view_checked(self):
        view_toggle = self.chkbox_pro_apps_view
        edit_toggle = self.chkbox_pro_apps_edit
        delete_toggle = self.chkbox_pro_apps_delete


        if view_toggle.isChecked() and edit_toggle.isChecked():
            view_toggle.setChecked(True)
            edit_toggle.setChecked(False)
        elif view_toggle.isChecked() and delete_toggle.isChecked():
            view_toggle.setChecked(True)
            delete_toggle.setChecked(False)

            
    
    # Handles the editing and deleting of the apps
    def get_app(self, app):
        delete = self.chk_delete_apps
        edit = self.chk_edit_apps
        is_protected_app = True if len(app) > 4 else False

        if delete.isChecked() and not is_protected_app:
            Model().delete('apps', app[0])
            self.update()
            delete.setChecked(False)
            
        elif edit.isChecked() and not is_protected_app:
            app_window = AppsEdit(app)
            app_window.app_edit_window_signal.connect(self.update)
            app_window.exec_()
            edit.setChecked(False)
        else:
            try:
                os.startfile(app[2])
            except OSError:
                pass


    def update(self):
        clear_window(self.gbox_apps)
        self.create_apps()
        self.read_styles()

    def login_clicked(self):
        if self.logged_in:
            self.login_signal.emit("logout requested")
        elif not self.logged_in:
            self.login_signal.emit("login requested")


    def login(self, signal):
        if signal == "logged in":
            self.btn_pro_apps_login.setText("Logout")
            self.logged_in = True
        elif signal == "logged out":
            self.btn_pro_apps_login.setText("Login")
            self.logged_in = False