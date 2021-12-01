import sys
import os

from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_widget import Ui_todo_tab
from PyQt5.QtWidgets import QWidget

from styles.tabs.todo import todo

from database.model import Model


class Todo_tab(QWidget, Ui_todo_tab):
    def __init__(self):
        super(Todo_tab, self).__init__()
        self.setupUi(self)
        self.read_style()

        self.btn_add_todo.clicked.connect(self.add_todo)
    
    def create_tab(self):
        return self

    def read_style(self):
        style = reduce(lambda a, b: a + b, todo)
        self.setStyleSheet(style)

    def add_todo(self):

        name = self.lne_add_todo.text()
        deadline = self.lbl_data_display.text()

        todo = {
            'name':name
        }
        Model().save("todos", todo)
        # print(Model.read("todos"))
        