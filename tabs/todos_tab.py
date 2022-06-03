import sys
import os
from datetime import date, datetime
from threading import Thread

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model
from designs.python.todo_widget import Ui_todo_tab
from widgets.todo_item import TodoItem
from utils.helpers import StyleSheet
from utils.message import Message
from integrations.calendar.c import Google_calendar
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.DateEdit import DateEdit
from widgetStyles.Calendar import Calendar
from utils.helpers import clear_window




class Todo_tab(QWidget, Ui_todo_tab):
    todo_signal = pyqtSignal(str)
    def __init__(self):
        super(Todo_tab, self).__init__()
        self.setupUi(self)
        self.read_style()
        self.display_todos()

        self.dte_date_select.setDate(date.today())

        self.btn_add_todo.clicked.connect(self.add_todo)
        self.dte_date_select.dateChanged.connect(self.get_date)

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
        self.lne_add_todo.setFont(QFont(font))
        self.btn_add_todo.setFont(QFont(font))
        self.lbl_date_display.setFont(QFont(font))
        self.dte_date_select.setFont(QFont(font))

    def add_todo(self):
        name = self.lne_add_todo.text()
        deadline = self.lbl_date_display.text() if self.lbl_date_display.text() != "Not Set" else None

        if(self.lbl_date_display.text()):
            deadline = self.dte_date_select.date().toPyDate()
            time = datetime.now()
            date = datetime(deadline.year, deadline.month, deadline.day, time.hour, time.minute, time.second)
            # Get the calendar integration setting
            calendar_integration = Model().read('settings')[0][6]
            # Check to see if the calendar integration should be used
            if(calendar_integration):
                th = Thread(target=google_thread, daemon=True, args=(date,))
                th.start()

        if not name:
            Message("Please enter a name for the todo.", "To-do").exec_()
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
        self.read_style()


# @concurrent.process(timeout=30)
def google_thread(date):
    Google_calendar.save(date)


        