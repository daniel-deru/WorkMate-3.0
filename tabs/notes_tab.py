import sys
import os
import math
import re
from functools import reduce

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from designs.python.notes_widget import Ui_notes_tab
from windows.notes_window import Note_window
from widgets.note_item import NoteItem
from utils.helpers import clear_window
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Widget import Widget
from widgetStyles.styles import color, default, mode
from utils.helpers import StyleSheet




class Notes_tab(QWidget, Ui_notes_tab):
    note_signal = pyqtSignal(str)
    def __init__(self):
        super(Notes_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.display_note()

        self.btn_note.clicked.connect(self.add_note)
        self.note_signal.connect(self.update_window)

    def create_tab(self):
        return self

    def read_styles(self):
        styles = [CheckBox, PushButton]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.btn_note.setFont(QFont(font))


    def add_note(self):
        note_window = Note_window()
        note_window.note_window_signal.connect(self.update_window)
        note_window.exec_()

    def display_note(self):
        clear_window(self.gbox_note_container)
        notes = Model().read("notes")
        grid_items = []
        for i in range(math.ceil(len(notes)/2)):
            subarr = []
            for j in range(2):
                if notes:
                    subarr.append(notes.pop(0))
            grid_items.append(subarr)
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                self.note = NoteItem(grid_items[i][j]).create()
                self.note.note_item_signal.connect(self.update_window)
                self.gbox_note_container.addWidget(self.note, row, col)
    
    def update_window(self):
        self.read_styles()
        self.display_note()
        # self.note.note_item_signal.emit("signal")
        





