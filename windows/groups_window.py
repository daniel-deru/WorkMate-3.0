import sys
import os
from json import dumps
from datetime import date, datetime, timedelta

from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.groups_window import Ui_GroupsWindow

from database.model import Model

from windows.group_window import GroupWindow

class GroupsWindow(Ui_GroupsWindow, QDialog):
    def __init__(self) -> None:
        super(GroupsWindow, self).__init__()
        self.setupUi(self)
        self.set_groups()
        
        self.btn_add_group.clicked.connect(self.add_group)
        
    def add_group(self):
        manage_group_window = GroupWindow()
        manage_group_window.group_add_signal.connect(self.set_groups)
        manage_group_window.exec_()
        
    def set_groups(self):
        groups = Model().read("groups")
        print(groups)