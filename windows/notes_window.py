import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QDialog, QWidget

from designs.python.note_window import Ui_Note_Window

from styles.windows.noteWindow import note_window_styles



class Note_window(QDialog, Ui_Note_Window):
    def __init__(self):
        super(Note_window, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(note_window_styles)


    