import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QListView
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

from database.model import Model

from windows.groups_window import GroupsWindow

class FilterGroupWidget(QWidget):
    group_changed_signal = pyqtSignal(int)
    def __init__(self) -> None:
        super(FilterGroupWidget, self).__init__()
        self.setupUi()
        self.show_groups()
        self.btn_manage_groups.clicked.connect(self.manage_groups)
        
        self.cmb_groups.currentIndexChanged.connect(self.filter)
        
    @pyqtSlot()
    def filter(self):
        self.group_changed_signal.emit(self.cmb_groups.currentData())
    
    @pyqtSlot()  
    def manage_groups(self):
        manage_groups_window = GroupsWindow()
        manage_groups_window.exec_()
        
    def setupUi(self):
        hbox = QHBoxLayout()
        
        self.cmb_groups = QComboBox()
        self.cmb_groups.setView(QListView())
        self.cmb_groups.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        
        self.btn_manage_groups = QPushButton("Manage Groups")
        self.btn_manage_groups.setCursor(QCursor(Qt.PointingHandCursor))
        
        hbox.addWidget(self.cmb_groups)
        hbox.addWidget(self.btn_manage_groups)
        
        self.setLayout(hbox)
        
    def show_groups(self):
        groups = Model().read("groups")
        for group in groups:
            self.cmb_groups.addItem(group[1], group[0])
            
    def get_current_group(self):
        return self.cmb_groups.currentData()
            
    