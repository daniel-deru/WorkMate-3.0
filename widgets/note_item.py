import sys
import os

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from windows.notes_window import Note_window
import assets.resources
from database.model import Model
from widgetStyles.Frame import Frame
from widgetStyles.Label import Label
from widgetStyles.PushButton import IconButton
from widgetStyles.styles import green
from utils.helpers import StyleSheet



class NoteItem(QFrame):
    note_item_signal = pyqtSignal(int)
    def __init__(self, note):
        super(NoteItem, self).__init__()
        self.note = note
        self.id = note[0]
        self.note_name = note[1]
        self.body = note[2]
        self.setupUI()
        self.read_styles()

        self.btn_delete.clicked.connect(self.delete_note)
        self.btn_edit.clicked.connect(self.edit_note)


    def setupUI(self):
        self.setObjectName("note_item")
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_note_item")
        # self.setMaximumWidth(200)

        self.name = QLabel(self.note_name)
        self.name.setObjectName("lbl_name")
        self.hbox.addWidget(self.name)
        self.setStyleSheet("border: none;")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hbox.addSpacerItem(self.HSpacer)

        self.btn_edit = QPushButton()
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setIcon(QIcon(":/other/edit.png"))
        self.btn_edit.setIconSize(QSize(20, 20))
        self.btn_edit.setStyleSheet(f"background-color: {green};")
        self.btn_edit.setCursor(QCursor(Qt.PointingHandCursor))
        self.hbox.addWidget(self.btn_edit)

        self.btn_delete = QPushButton()
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setIcon(QIcon(":/other/delete.png"))
        self.btn_delete.setIconSize(QSize(20, 20))
        self.btn_delete.setStyleSheet(f"background-color: {green};")
        self.btn_delete.setCursor(QCursor(Qt.PointingHandCursor))
        self.hbox.addWidget(self.btn_delete)

        self.setLayout(self.hbox)


    def create(self):
        return self
    
    def delete_note(self):
        Model().delete("notes", self.id)
        self.note_item_signal.emit(self.id)

    def edit_note(self):
        edit_window = Note_window(self.note)
        edit_window.note_window_signal.connect(lambda: self.note_item_signal.emit(self.id))
        edit_window.exec_()

    def read_styles(self):
        styles = [
            Frame,
            Label,
            IconButton
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read("settings")[0][2]
        self.name.setFont(QFont(font))
        
        
