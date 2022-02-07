import os
import sys

from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.helpers import StyleSheet
from utils.message import Message
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Dialog import Dialog
from widgetStyles.Label import Label
from database.model import Model

from designs.python.apps_edit_window import Ui_AppsEdit

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

class AppsEdit(QDialog, Ui_AppsEdit):
    app_edit_window_signal = pyqtSignal(str)
    def __init__(self, app):
        super(AppsEdit, self).__init__()
        self.app = app
        self.setupUi(self)
        self.read_styles()
        self.fill_fields()
        self.apps = Model().read("apps")

        self.spnbox_index.setValue(len(self.apps))
        self.spnbox_index.setMaximum(len(self.apps))
        self.spnbox_index.setMinimum(1)

        self.btn_discard.clicked.connect(lambda: self.close())
        self.btn_desktop.clicked.connect(self.add_from_desktop)
        self.btn_save.clicked.connect(self.save_clicked)
    
    def read_styles(self):
        styles = [
            PushButton,
            LineEdit,
            SpinBox,
            Dialog,
            Label
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def fill_fields(self):
        name = self.lnedt_name
        path = self.lnedt_path
        sequence = self.spnbox_index

        name.setText(self.app[1])
        path.setText(self.app[2])
        sequence.setValue(self.app[3])


    def add_from_desktop(self):
        file = QFileDialog.getOpenFileName(self, "Open a file", DESKTOP, "All Files (*.*)")[0]
        path = self.lnedt_path
        path.setText(file)


    def save_clicked(self):
        name = self.lnedt_name.text()
        path = self.lnedt_path.text()
        sequence = self.spnbox_index.value()

        

        data = {
                    'name': name,
                    'path': path,
                    'sequence': sequence,
                }
            

        if not name:
            Message("Please enter a name for your app", "No name").exec_()
            return
        elif not path:
            Message("Please enter a path for your app", "No path").exec_()
            return
        else:
            
            if self.app is not None:
                if self.app[3] != sequence:
                    old = self.app[3] - 1
                    new = sequence - 1
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
                self.app_edit_window_signal.emit("updated")
            self.close()

    
