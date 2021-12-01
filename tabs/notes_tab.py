import sys
import os

from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.notes_widget import Ui_notes_tab
from PyQt5.QtWidgets import QWidget

from styles.tabs.notes import notes

from windows.notes_window import Note_window


class Notes_tab(QWidget, Ui_notes_tab):
    def __init__(self):
        super(Notes_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.btn_note.clicked.connect(self.add_note)

    def create_tab(self):
        return self

    def read_styles(self):
        style = reduce(lambda a, b: a + b, notes)
        self.setStyleSheet(style)

    def add_note(self):
        note_window = Note_window()
        note_window.exec_()