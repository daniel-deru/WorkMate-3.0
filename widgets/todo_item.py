import sys
import os
from functools import reduce
import re

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

from widgetStyles.Frame import TodoFrameComplete, TodoFrameDelete
from widgetStyles.Label import Label, LabelMono
from widgetStyles.PushButton import IconButton
from utils.helpers import StyleSheet



class TodoItem(QFrame):
    todo_item_signal = pyqtSignal(str)
    def __init__(self, todo):
        super(TodoItem, self).__init__()
        self.todo_id = todo[0]
        self.todo = todo[1]
        self.completed = todo[2]
        self.date = todo[3]
        self.setupUI()
        self.read_styles()

        # self.action.clicked.connect(self.button_clicked)

    
    def create_widget(self):
        return self

  
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
                if self.completed:
                    Model().delete("todos", self.todo_id)
                else:
                    Model().update("todos", {'complete': 1}, self.todo_id)
        self.todo_item_signal.emit(self.todo)
        

    
    def setupUI(self):
        self.setObjectName("TodoItem")

        
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_todo_item")

        self.name = QLabel(self.todo)
        self.name.setObjectName("lbl_todo_name")
        self.name.setStyleSheet("color: #ffffff")

        self.date = QLabel(self.date)
        self.date.setObjectName("lbl_date")
        self.date.setStyleSheet("color: #ffffff")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        icon = QIcon("assets/delete.png") if self.completed else QIcon("assets/done.png")
        self.action = QPushButton()
        self.action.setObjectName("btn_action")
        self.action.setIcon(icon)
        self.action.setIconSize(QSize(15, 15))



        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.date)
        self.hbox.addSpacerItem(self.HSpacer)
        self.hbox.addWidget(self.action)

        self.setLayout(self.hbox)


    def read_styles(self):
        Background = TodoFrameDelete if self.completed else TodoFrameComplete
        styles = [
            LabelMono,
            IconButton,
            Background
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)




