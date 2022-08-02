import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy, QWidget
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QCursor


class GroupWidget(QWidget):
    def __init__(self, group_data) -> None:
        super(GroupWidget, self).__init__()