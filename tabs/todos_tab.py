import sys
import os
from datetime import date, datetime
from threading import Thread
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from designs.python.todo_widget import Ui_todo_tab

from widgets.todo_item import TodoItem

from utils.helpers import StyleSheet
from utils.message import Message
from utils.helpers import clear_window

from integrations.calendar.c import Google

from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.DateEdit import DateEdit
from widgetStyles.Calendar import Calendar

from windows.todo_window import TodoWindow





class Todo_tab(Ui_todo_tab, QWidget):
    todo_signal = pyqtSignal(str)
    def __init__(self):
        super(Todo_tab, self).__init__()
        self.setupUi(self)
        self.read_style()
        self.display_todos()

        self.btn_add_todo.clicked.connect(self.add_todo)

        self.todo_signal.connect(self.update)
    
    def create_tab(self):
        return self

    def read_style(self):
        styles = [
            PushButton,
            LineEdit,
            Label,
            DateEdit,
            Calendar,
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.btn_add_todo.setFont(QFont(font))

    def add_todo(self):
        todo_window = TodoWindow()
        todo_window.todo_edit_signal.connect(self.update)
        todo_window.exec_()


    def display_todos(self):

        todos = Model().read("todos")

        for i in range(len(todos)):
            self.todo_item = TodoItem(todos[i]).create_widget()
            self.todo_item.todo_item_signal.connect(self.update)
            # self.vbox_todo_container.addWidget(self.todo_item)
            
        COLUMNS = 2
        grid_items = []
        for i in range(math.ceil(len(todos)/COLUMNS)):
            subarr = []
            for j in range(COLUMNS):
                if todos:
                    subarr.append(todos.pop(0))
            grid_items.append(subarr)
            
        for i in range(len(grid_items)):
            row = i
            for j in range(len(grid_items[i])):
                col = j
                self.todo_item = TodoItem(grid_items[i][j]).create_widget()
                self.todo_item.todo_item_signal.connect(self.update)
                self.todo_container.addWidget(self.todo_item, row, col)
    
    def update(self):
        clear_window(self.todo_container)
        self.display_todos()
        self.read_style()


# @concurrent.process(timeout=30)
def google_thread(date, message):
    Google.save(date, message)


        