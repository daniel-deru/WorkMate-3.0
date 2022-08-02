import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon


from designs.python.group_window import Ui_GroupWindow

from utils.message import Message

from database.model import Model

class GroupWindow(Ui_GroupWindow, QDialog):
    group_add_signal = pyqtSignal(bool)
    def __init__(self) -> None:
        super(GroupWindow, self).__init__()
        self.setupUi(self)
        
        self.btn_discard.clicked.connect(self.close)
        self.btn_save.clicked.connect(self.add_group)
    
    @pyqtSlot()
    def add_group(self):
        name = self.lne_name.text()
        description = self.lne_description.toPlainText()
        
        if not name:
            Message("Please enter a name for the group", "Missing Group Name").exec_()
            
        group = {
            "name": name,
            "description": description
        }
            
        Model().save("groups", group)
        self.group_add_signal.emit(True)
        self.close()
            
        
        
        