from ast import Load
import sys
import os

from PyQt5.QtWidgets import QDialog, QLabel, QSpacerItem, QSizePolicy, QToolButton, QCheckBox, QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
import pyperclip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.loading import Ui_Dialog


class LoadingScreen(Ui_Dialog, QDialog):
    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.setupUi(self)
        
        