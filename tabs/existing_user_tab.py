import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QWidget

from designs.python.existing_user_tab import Ui_ExistingUser

class ExistingUserTab(Ui_ExistingUser, QWidget):
    def __init__(self) -> None:
        super(ExistingUserTab, self).__init__()
        self.setupUi(self)
        
    def create_tab(self):
        return self