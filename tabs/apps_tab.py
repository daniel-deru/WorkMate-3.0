import sys
import os
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.apps_tab import Ui_apps_tab
from windows.apps_window import Apps_window
from database.model import Model
from widgets.app_item import AppItem
from utils.helpers import clear_window
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from utils.helpers import StyleSheet

class Apps_tab(QWidget, Ui_apps_tab):
    app_signal = pyqtSignal(str)
    table_signal = pyqtSignal(str)
    def __init__(self):
        super(Apps_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        
        self.create_apps()
        self.create_protected_apps()

        self.btn_add_app.clicked.connect(self.add_app)
        self.chk_edit_apps.stateChanged.connect(self.edit_checked)
        self.chk_delete_apps.stateChanged.connect(self.delete_checked)
        self.chkbox_pro_apps_edit.stateChanged.connect(self.edit_checked)
        self.chkbox_pro_apps_delete.stateChanged.connect(self.delete_checked)
        

        self.app_signal.connect(self.update)
    
    def create_tab(self):
        return self

    def read_styles(self):
        styles = [CheckBox, PushButton]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.btn_add_app.setFont(QFont(font))
        self.chk_edit_apps.setFont(QFont(font))
        self.chk_delete_apps.setFont(QFont(font))


    def add_app(self):
        app_window = Apps_window()
        app_window.app_window_signal.connect(self.update)
        app_window.exec_()
    
    def create_apps(self):
        apps = Model().read('apps')
        COLUMNS = 2
        sorted_apps = sorted(apps, key=lambda item: item[COLUMNS])
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

    def create_protected_apps(self):
        apps = Model().read('protected_apps')
        COLUMNS = 2
        sorted_apps = sorted(apps, key=lambda item: item[COLUMNS])
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
                self.gbox_pro_apps.addWidget(app_button, row, col)

    def edit_checked(self):
        delete_apps = self.chk_delete_apps
        edit_apps = self.chk_edit_apps
        pro_delete_apps = self.chkbox_pro_apps_delete
        pro_edit_apps = self.chkbox_pro_apps_edit

        if delete_apps.isChecked() and edit_apps.isChecked():
            edit_apps.setChecked(True)
            delete_apps.setChecked(False)
            pro_delete_apps.setChecked(False)
            pro_edit_apps.setChecked(False)

        elif pro_delete_apps.isChecked() and pro_edit_apps.isChecked():
            pro_edit_apps.setChecked(True)
            pro_delete_apps.setChecked(False)
            edit_apps.setChecked(False)
            delete_apps.setChecked(False)
 

    def delete_checked(self):
        delete_apps = self.chk_delete_apps
        edit_apps = self.chk_edit_apps
        pro_delete_apps = self.chkbox_pro_apps_delete
        pro_edit_apps = self.chkbox_pro_apps_edit

        if edit_apps.isChecked() and delete_apps.isChecked():
            delete_apps.setChecked(True)
            edit_apps.setChecked(False)
            pro_edit_apps.setChecked(False)
            pro_delete_apps.setChecked(False)

        elif pro_edit_apps.isChecked() and pro_delete_apps.isChecked():
            pro_delete_apps.setChecked(True)
            pro_edit_apps.setChecked(False)
            delete_apps.setChecked(False)
            edit_apps.setChecked(False)
    
    # Handles the editing and deleting of the apps
    def get_app(self, app):
        delete = self.chk_delete_apps
        edit = self.chk_edit_apps
        pro_delete = self.chkbox_pro_apps_delete
        pro_edit = self.chkbox_pro_apps_edit
        is_protected_app = app[4]

        if delete.isChecked() and not is_protected_app:
            Model().delete('apps', app[0])
            self.update()
            delete.setChecked(False)
            
        elif edit.isChecked() and not is_protected_app:
            app_window = Apps_window(app)
            app_window.app_window_signal.connect(self.update)
            app_window.exec_()
            edit.setChecked(False)
        # app[4] tests to see if the app is open or protected
        elif pro_delete.isChecked() and is_protected_app:
            Model().delete('protected_apps', app[0])
            self.update()
            delete.setChecked(False)
        # app[4] tests to see if the app is open or protected
        elif pro_edit.isChecked() and is_protected_app:
            app_window = Apps_window(app)
            app_window.app_window_signal.connect(self.update)
            app_window.exec_()
            edit.setChecked(False)
        else:
            try:
                os.startfile(app[2])
            except OSError:
                pass


    def update(self):
        clear_window(self.gbox_apps)
        clear_window(self.gbox_pro_apps)
        self.create_apps()
        self.create_protected_apps()
        self.read_styles()


        

