import os
import sys

from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab

class Vault_tab(QWidget, Ui_Vault_tab):
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
     
    
    def create_tab(self):
        return self




