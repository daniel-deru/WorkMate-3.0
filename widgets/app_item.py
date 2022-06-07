import os
import sys

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QCursor


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

class AppItem(QPushButton):
    app_clicked_signal = pyqtSignal(tuple)
    def __init__(self, app):
        super(AppItem, self).__init__()
        self.app = app
        self.setupUI()

        self.adjustSize()
        

        self.clicked.connect(self.app_clicked)

    def app_clicked(self):
        self.app_clicked_signal.emit(self.app)

    def create(self):
        return self
    
    def setupUI(self):
        self.setText(self.app[1])
        font = Model().read("settings")[0][2]
        self.setFont(QFont(font))

        self.setCursor(QCursor(Qt.PointingHandCursor))