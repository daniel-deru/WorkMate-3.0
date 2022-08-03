import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QWidget, QToolButton
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QCursor

from database.model import Model

from windows.group_view_window import GroupViewWindow
from windows.group_window import GroupWindow

from utils.message import Message


class GroupWidget(QWidget):
    def __init__(self, group, group_data) -> None:
        super(GroupWidget, self).__init__()
        self.group = group
        self.group_data = group_data
        
        self.total = 0
        for feature in self.group_data:
            self.total += len(self.group_data[feature])
        
        self.setupUi()
        
        self.btn_view.clicked.connect(self.view_group)
        self.btn_edit.clicked.connect(self.edit_group)
        
    @pyqtSlot()
    def edit_group(self):
        if self.group[1] == "Ungrouped":
            Message("You cannot edit this group since it is the default group", "Cannot edit this group").exec_()
        else:
            edit_group = GroupWindow(self.group)
            edit_group.exec_()
            
        
    @pyqtSlot()
    def view_group(self):
        view_group = GroupViewWindow(self.group, self.group_data)
        view_group.exec_()
        
    def setupUi(self):
        dark_mode_on = int(Model().read('settings')[0][1])
        
        self.hbox = QHBoxLayout()
        
        self.lbl_group = QLabel(self.group[1])
        self.lbl_group.setFixedWidth(200)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.lbl_count = QLabel(str(self.total))
        
        color = "white" if dark_mode_on else "black"
        self.btn_view = QToolButton()
        self.btn_view.setIcon(QIcon(f":/input/eye_{color}_open.svg"))
        
        edit_icon = "edit.svg" if dark_mode_on else "edit_black"
        self.btn_edit = QToolButton()
        self.btn_edit.setIcon(QIcon(f":/other/{edit_icon}"))
        
        
        self.hbox.addWidget(self.lbl_group)
        self.hbox.addWidget(self.lbl_count)
        self.hbox.addSpacerItem(spacer)
        self.hbox.addWidget(self.btn_view)
        self.hbox.addWidget(self.btn_edit)
        
        self.setLayout(self.hbox)