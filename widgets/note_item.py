import sys
import os
from functools import reduce

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from styles.widgets.Frame import Frame
from styles.widgets.Label import Label
from styles.widgets.PushButton import IconButton
from windows.notes_window import Note_window


class NoteItem(QFrame):
    note_item_signal = pyqtSignal(int)
    def __init__(self, note):
        super(NoteItem, self).__init__()
        self.note = note
        self.id = note[0]
        self.note_name = note[1]
        self.body = note[2]
        self.setupUI()

        self.btn_delete.clicked.connect(self.delete_note)
        self.btn_edit.clicked.connect(self.edit_note)
        

    def setupUI(self):
        self.setObjectName("note_item")
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_note_item")

        self.name = QLabel(self.note_name)
        self.name.setObjectName("lbl_name")
        self.hbox.addWidget(self.name)
        self.setStyleSheet("border: none;")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hbox.addSpacerItem(self.HSpacer)

        self.btn_edit = QPushButton()
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setIcon(QIcon("assets/edit.png"))
        self.btn_edit.setIconSize(QSize(20, 20))
        self.hbox.addWidget(self.btn_edit)

        self.btn_delete = QPushButton()
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setIcon(QIcon("assets/delete-red.png"))
        self.btn_delete.setIconSize(QSize(20, 20))
        self.hbox.addWidget(self.btn_delete)

        self.setLayout(self.hbox)
        styles = [
            Frame,
            Label,
            IconButton
            ]
        self.setStyleSheet(reduce(lambda a, b: a + b, styles))

    def create(self):
        return self
    
    def delete_note(self):
        Model().delete("notes", self.id)
        self.note_item_signal.emit(self.id)

    def edit_note(self):
        edit_window = Note_window(self.note)
        edit_window.note_window_signal.connect(lambda: self.note_item_signal.emit(self.id))
        edit_window.exec_()
        
        
