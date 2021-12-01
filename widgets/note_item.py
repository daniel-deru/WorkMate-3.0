import sys
import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from styles.widgets.NoteWidget import NoteWidget


class NoteItem(QWidget):
    def __init__(self):
        super(NoteItem, self).__init__()
        self.setupUI()
        

    def setupUI(self):
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_note_item")

        self.name = QLabel("Note Name")
        self.name.setObjectName("lbl_name")
        self.hbox.addWidget(self.name)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("btn_delete")
        self.hbox.addWidget(self.btn_delete)

        self.setLayout(self.hbox)
        self.setStyleSheet(NoteWidget)

    def create(self):
        return self