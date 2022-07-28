import os
import sys
from datetime import date, datetime, timedelta

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import QDate, Qt, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_edit_window import Ui_todo_edit

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm
from widgetStyles.ComboBox import ComboBox
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.Widget import Widget
from widgetStyles.TextEdit import TextEdit


from database.model import Model
from utils.helpers import StyleSheet

class TodoWindow(Ui_todo_edit, QDialog):
    todo_edit_signal = pyqtSignal(str)
    def __init__(self, todo=None):
        super(TodoWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.cmbx_status.setCursor(QCursor(Qt.PointingHandCursor))
        self.read_styles()
        self.todo: object or None = todo
        
        self.dtedt_date.setDate(date.today())
        if self.todo: self.set_data()

        # self.dtedt_date.dateChanged.connect(self.get_date)
        # self.cmbx_status.currentIndexChanged.connect(self.get_status)
        self.btn_save.clicked.connect(self.save_clicked)

    def read_styles(self):
        widget_list = [
            Dialog,
            PushButton,
            LineEdit,
            Label,
            ComboBox,
            DateEditForm,
            Calendar,
            TextEdit
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
            self.lnedt_name,
            self.lbl_description,
            self.txe_description
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
            
        self.dtedt_date.setFont(QFont(font_name, 5))
        

    
    def set_data(self):
        self.btn_save.setText("Update")
        if self.todo:
            self.lnedt_name.setText(self.todo[1])
            self.txe_description.setPlainText(self.todo[4])
            
            deadline_datetime = datetime.strptime(self.todo[3], "%Y-%m-%d")
            deadline = date(deadline_datetime.year, deadline_datetime.month, deadline_datetime.day)
            self.dtedt_date.setDate(deadline)
            
            self.cmbx_status.setCurrentIndex(int(self.todo[2]))
            

    def save_clicked(self):
        name: str = self.lnedt_name.text()
        description: str = self.txe_description.toPlainText()
        deadline: date = self.dtedt_date.date().toPyDate()
        
        deadline_text: str = datetime.strftime(deadline, "%Y-%m-%d")
        
        status_text = self.cmbx_status.currentText()
        status = "1" if status_text == "Complete" else "0"
        
            
        data = {
            'name': name, 
            'complete': status, 
            'deadline': deadline_text,
            'description': description
        }

        if self.todo:
            Model().update('todos', data, self.todo[0])
        else:
            Model().save("todos", data)
        self.todo_edit_signal.emit("updated todo")
        self.close()
        

    def get_date(self):
        date = self.dtedt_date.date().toPyDate()
        self.todo['date'] = date
    
    def get_status(self):
        status: int = self.cmbx_status.currentIndex()
        self.todo['status'] = status
            
        