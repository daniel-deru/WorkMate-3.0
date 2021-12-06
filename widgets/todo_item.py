import sys
import os
from functools import reduce

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model


from styles.widgets.Frame import TodoFrameComplete, TodoFrameDelete
from styles.widgets.Label import Label
from styles.widgets.PushButton import IconButton


class TodoItem(QFrame):
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
            Model().delete("todos", self.todo_id)
        else:
            Model().update("todos", {'complete': 1}, self.todo_id)
            
            
        self.todo_item_signal.emit(self.todo)
        

    
    def setupUI(self):
        self.setObjectName("TodoItem")

        Frame = TodoFrameDelete if self.completed else TodoFrameComplete

        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_todo_item")

        self.name = QLabel(self.todo)
        self.name.setObjectName("lbl_todo_name")

        self.date = QLabel(self.date)
        self.date.setObjectName("lbl_date")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)


        icon = QIcon("assets/delete.png") if self.completed else QIcon("assets/done.png")
        self.action = QPushButton()
        self.action.setObjectName("btn_action")
        self.action.setIcon(icon)
        self.action.setIconSize(QSize(30, 30))



        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.date)
        self.hbox.addSpacerItem(self.HSpacer)
        self.hbox.addWidget(self.action)

        self.setLayout(self.hbox)

        styles = [
            Frame,
            Label,
            IconButton
        ]

        self.setStyleSheet(reduce(lambda a, b: a + b, styles))




