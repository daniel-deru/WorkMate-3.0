import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QWidget, QToolButton
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QCursor

from database.model import Model

from windows.group_view_window import GroupViewWindow


class GroupWidget(QWidget):
    def __init__(self, group) -> None:
        super(GroupWidget, self).__init__()
        self.group = group
        self.setupUi()
        
        self.btn_view.clicked.connect(self.view_group)
        
    @pyqtSlot()
    def view_group(self):
        view_group = GroupViewWindow(self.group)
        view_group.exec_()
        
    def setupUi(self):
        dark_mode_on = int(Model().read('settings')[0][1])
        
        self.hbox = QHBoxLayout()
        
        self.lbl_group = QLabel(self.group[1])
        
        color = "white" if dark_mode_on else "black"
        self.btn_view = QToolButton()
        self.btn_view.setIcon(QIcon(f":/input/eye_{color}_open.svg"))
        
        edit_icon = "edit.svg" if dark_mode_on else "edit_black"
        self.btn_edit = QToolButton()
        self.btn_edit.setIcon(QIcon(f":/other/{edit_icon}"))
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.hbox.addWidget(self.lbl_group)
        self.hbox.addSpacerItem(spacer)
        self.hbox.addWidget(self.btn_view)
        self.hbox.addWidget(self.btn_edit)
        
        self.setLayout(self.hbox)