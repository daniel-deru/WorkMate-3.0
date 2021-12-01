import sys
import os

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model


class TodoItem(QWidget):
    todo_item_signal = pyqtSignal(str)
    def __init__(self, todo):
        super(TodoItem, self).__init__()
        self.todo_id = todo[0]
        self.todo = todo[1]
        self.completed = todo[2]
        self.date = todo[3]
        self.setupUI()

        self.action.clicked.connect(self.button_clicked)
        

    
    def create_widget(self):
        return self

    def button_clicked(self):
        if self.completed:
            Model().delete("todos", self.todo)
        else:
            Model().update("todos", "complete", 1, self.todo)

            
        self.todo_item_signal.emit(self.todo)
        

    
    def setupUI(self):
        self.setObjectName("TodoItem")

        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_todo_item")

        self.name = QLabel(self.todo)
        self.name.setObjectName("lbl_todo_name")

        self.date = QLabel(self.date)
        self.date.setObjectName("lbl_date")

        label = "Delete" if self.completed else "Complete"
        self.action = QPushButton(label)
        self.action.setObjectName("btn_action")

        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.date)
        self.hbox.addWidget(self.action)

        self.setLayout(self.hbox)



