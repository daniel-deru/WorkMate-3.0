import os
import sys

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

class VaultItem(QPushButton):
    vault_clicked_signal = pyqtSignal(tuple)
    def __init__(self, secret):
        super(VaultItem, self).__init__()
        self.secret = secret
        self.setupUI()
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        if(len(self.text()) > 25): self.setStyleSheet("text-align: left;")
        self.clicked.connect(self.app_clicked)

    def app_clicked(self):
        self.vault_clicked_signal.emit(tuple(self.secret))

    def create(self):
        return self
    
    def setupUI(self):
        self.setText(self.secret[2])
        font = Model().read("settings")[0][2]
        self.setFont(QFont(font))
        # self.setAlign
        