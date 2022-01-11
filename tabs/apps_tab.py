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

        self.btn_add_app.clicked.connect(self.add_app)
        self.chk_edit_apps.stateChanged.connect(self.edit_checked)
        self.chk_delete_apps.stateChanged.connect(self.delete_checked)

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
        sorted_apps = sorted(apps, key=lambda item: item[3])
        grid_items = []
        for i in range(math.ceil(len(sorted_apps)/3)):
            subarr = []
            for j in range(3):
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
        if self.chk_delete_apps.isChecked() and self.chk_edit_apps.isChecked():
            self.chk_delete_apps.setChecked(False)
            self.chk_edit_apps.setChecked(True)
 

    def delete_checked(self):
        if self.chk_edit_apps.isChecked() and self.chk_delete_apps.isChecked():
            self.chk_edit_apps.setChecked(False)
            self.chk_delete_apps.setChecked(True)
    
    def get_app(self, app):
        delete = self.chk_delete_apps
        edit = self.chk_edit_apps
        if delete.isChecked():
            Model().delete('apps', app[0])
            self.update()
            delete.setChecked(False)
            
        elif edit.isChecked():
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
        self.create_apps()
        self.read_styles()
        apps = Model().read("apps")[0]
        print(apps)
        # self.table_signal.emit("update")

        






# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     apps_tab = QWidget()
#     ui = Ui_apps_tab()
#     ui.setupUi(apps_tab)
#     apps_tab.show()
#     sys.exit(app.exec_())

