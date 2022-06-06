import os
import sys

from PyQt5.QtWidgets import QDialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_edit_window import Ui_todo_edit

class TodoEditWindow(Ui_todo_edit, QDialog):
    def __init__(self):
        super(TodoEditWindow, self).__init__()
        self.setupUi(self)