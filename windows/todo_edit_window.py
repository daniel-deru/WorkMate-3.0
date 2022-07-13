import os
import sys

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import QDate, Qt, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_edit_window import Ui_todo_edit

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEdit
from widgetStyles.ComboBox import ComboBox
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.DateEdit import DateEdit
from widgetStyles.Widget import Widget


from database.model import Model
from utils.helpers import StyleSheet

class TodoEditWindow(Ui_todo_edit, QDialog):
    todo_edit_signal = pyqtSignal(str)
    def __init__(self, todo=None):
        super(TodoEditWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmbx_status.setCursor(QCursor(Qt.PointingHandCursor))
        self.read_styles()
        self.todo: object = todo
        
        self.set_data()

        self.dtedt_date.dateChanged.connect(self.get_date)
        self.cmbx_status.currentIndexChanged.connect(self.get_status)
        self.btn_save.clicked.connect(self.save_clicked)

    def read_styles(self):
        widget_list = [
            Widget,
            Dialog,
            PushButton,
            LineEdit,
            Label,
            ComboBox,
            DateEdit,
            Calendar,
        ]

        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        font_name: str = Model().read("settings")[0][2]

        font_widgets = [
            self.lbl_name,
            self.lbl_date,
            self.lbl_status,
            self.btn_save,
            self.cmbx_status,
            self.dtedt_date,
            self.lnedt_name
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
            
        self.dtedt_date.setFont(QFont(font_name, 5))
        

    
    def set_data(self):
        if self.todo:
            self.lnedt_name.setText(self.todo['name'])

            date: list[str] = self.todo['date'].split("-")
            self.dtedt_date.setDate(QDate(int(date[0]), int(date[1]), int(date[2])))

            if(self.todo['status']):
                self.cmbx_status.setCurrentIndex(1)
            else:
                self.cmbx_status.setCurrentIndex(0)

    def save_clicked(self):
        if(self.todo['name'] != self.lnedt_name.text()):
            self.todo['name'] = self.lnedt_name.text()

        Model().update('todos', {'name': self.todo['name'], 'complete': self.todo['status'], 'deadline': self.todo['date']}, self.todo['id'])
        self.todo_edit_signal.emit("updated todo")
        self.close()
        

    def get_date(self):
        date = self.dtedt_date.date().toPyDate()
        self.todo['date'] = date
    
    def get_status(self):
        status: int = self.cmbx_status.currentIndex()
        self.todo['status'] = status
            
        