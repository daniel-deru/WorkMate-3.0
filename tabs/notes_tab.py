import sys
import os

from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.notes_widget import Ui_notes_tab
from PyQt5.QtWidgets import QWidget

from styles.tabs.notes import notes

from windows.notes_window import Note_window

from widgets.note_item import NoteItem


class Notes_tab(QWidget, Ui_notes_tab):
    def __init__(self):
        super(Notes_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.display_note()

        self.btn_note.clicked.connect(self.add_note)

    def create_tab(self):
        return self

    def read_styles(self):
        style = reduce(lambda a, b: a + b, notes)
        self.setStyleSheet(style)

    def add_note(self):
        note_window = Note_window()
        note_window.exec_()

    def display_note(self):
        
        column_switcher = True
        for i in range(5):
            column = 0
            if column_switcher:
                column = 0
                column_switcher = False
            else:
                column = 1
                column_switcher = True
            note = NoteItem().create()
            self.gbox_note_container.addWidget(note, i, column)

#   0     0   # 0   1
#   1     0   # 1   1
#   2     0   # 2   1
#   3     0   # 3   1

