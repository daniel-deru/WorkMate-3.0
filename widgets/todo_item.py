import sys
import os

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QToolButton
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

from widgetStyles.Frame import TodoFrameComplete, TodoFrameDelete
from widgetStyles.Label import LabelMono
from widgetStyles.ToolButton import ToolButton
from utils.helpers import StyleSheet

from windows.todo_edit_window import TodoEditWindow



class TodoItem(QFrame):
    todo_item_signal = pyqtSignal(str)
    def __init__(self, todo):
        super(TodoItem, self).__init__()
        self.todo_id = todo[0]
        self.todo = todo[1]
        self.completed = int(todo[2])
        self.date = todo[3]
        self.setupUI()
        self.read_styles()

        self.editButton.clicked.connect(self.editButtonClick)
        self.statusButton.clicked.connect(self.state_change_button_clicked)

    
    def create_widget(self):
        return self        

    
    def setupUI(self):
        self.setObjectName("TodoItem")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.hbox = QHBoxLayout()
        self.hbox.setObjectName("hbox_todo_item")

        self.name = QLabel(self.todo)
        self.name.setObjectName("lbl_todo_name")
        self.name.setStyleSheet("color: #ffffff")

        self.lbl_date = QLabel(self.date)
        self.lbl_date.setObjectName("lbl_date")
        self.lbl_date.setStyleSheet("color: #ffffff")

        self.HSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        editIcon = QIcon("./assets/edit.png")
        self.editButton = QToolButton()
        self.editButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.editButton.setObjectName("btn_edit")
        self.editButton.setIcon(editIcon)
        self.editButton.setIconSize(QSize(20, 20))
        self.editButton.setCursor(QCursor(Qt.PointingHandCursor))

        icon = QIcon("./assets/delete.png") if self.completed else QIcon("./assets/done.png")
        self.statusButton = QToolButton()

        self.statusButton.setObjectName("btn_status")
        self.statusButton.setIcon(icon)
        self.statusButton.setIconSize(QSize(20, 20))
        self.statusButton.setCursor(QCursor(Qt.PointingHandCursor))



        self.hbox.addWidget(self.name)
        self.hbox.addWidget(self.lbl_date)
        # self.hbox.addSpacerItem(self.HSpacer)
        self.hbox.addWidget(self.editButton)
        self.hbox.addWidget(self.statusButton)

        self.setLayout(self.hbox)


    def read_styles(self):
        Background = TodoFrameDelete if self.completed else TodoFrameComplete
        styles = [
            LabelMono,
            Background,
            ToolButton
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read("settings")[0][2]
        self.name.setFont(QFont(font))
        self.lbl_date.setFont(QFont(font))
    
    def state_change_button_clicked(self):
        if self.completed:
            Model().delete("todos", self.todo_id)
        else:
            Model().update("todos", {'complete': "1"}, self.todo_id)
        self.todo_item_signal.emit(self.todo)

    # Fire an event when the edit button is clicked
    def editButtonClick(self):
        todo_data = {
            'name': self.todo,
            'date': self.date,
            'status': self.completed,
            'id': self.todo_id
        }
        todoEditWindow = TodoEditWindow(todo_data)
        todoEditWindow.todo_edit_signal.connect(self.update)
        todoEditWindow.exec_()

    # send signal to the main tab to update the view
    def update(self):
        self.todo_item_signal.emit(self.todo)


