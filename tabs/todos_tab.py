import sys
import os
from datetime import date
from functools import reduce

from PyQt5.QtWidgets import QWidget

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from designs.python.todo_widget import Ui_todo_tab
from widgets.todo_item import TodoItem
from utils.helpers import clear_window
from utils.message import Message
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.DateEdit import DateEdit
from widgetStyles.Widget import Widget
from widgetStyles.Calendar import Calendar

styles = [
    Widget,
    PushButton,
    LineEdit,
    Label,
    DateEdit,
    Calendar,
]

class Todo_tab(QWidget, Ui_todo_tab):
    def __init__(self):
        super(Todo_tab, self).__init__()
        self.setupUi(self)
        self.read_style()
        self.display_todos()

        self.dte_date_select.setDate(date.today())

        self.btn_add_todo.clicked.connect(self.add_todo)
        self.dte_date_select.dateChanged.connect(self.get_date)
    
    def create_tab(self):
        return self

    def read_style(self):
        self.setStyleSheet(reduce(lambda a, b: a + b, styles))

    def add_todo(self):
        name = self.lne_add_todo.text()
        deadline = self.lbl_date_display.text() if self.lbl_date_display.text() != "Not Set" else None

        if not name:
            Message("Please enter a name for the todo.", "Todo").exec_()
        else:
            todo = {
                'name':name,
                'deadline': deadline
            }
            Model().save("todos", todo)
            self.update()
        self.lne_add_todo.clear()


    def display_todos(self):
        todos = Model().read("todos")
        for i in range(len(todos)):
            self.todo_item = TodoItem(todos[i]).create_widget()
            self.todo_item.todo_item_signal.connect(self.update)
            self.vbox_todo_container.addWidget(self.todo_item)

    def get_date(self):
        deadline = self.dte_date_select.date().toPyDate()
        self.lbl_date_display.setText(str(deadline))
    
    def update(self):
        clear_window(self.vbox_todo_container)
        self.display_todos()


        