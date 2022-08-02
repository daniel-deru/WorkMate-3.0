import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog

from designs.python.group_view_window import Ui_GroupWindow

class GroupViewWindow(Ui_GroupWindow, QDialog):
    def __init__(self, group) -> None:
        super(GroupViewWindow, self).__init__()
        self.group = group
        self.setupUi(self)
        self.display_data()
        
    def display_data(self):
        self.lbl_group_name.setText(self.group[1])
        self.lbl_description.setText(self.group[2])
        
    
        
    
