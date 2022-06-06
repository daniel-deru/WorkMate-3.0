import os
import sys

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.todo_edit_window import Ui_todo_edit

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEdit
from widgetStyles.ComboBox import ComboBox
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog


from database.model import Model
from utils.helpers import StyleSheet

class TodoEditWindow(Ui_todo_edit, QDialog):
    def __init__(self):
        super(TodoEditWindow, self).__init__()
        self.setupUi(self)
        self.read_styles()

    def read_styles(self):
        widget_list = [
            PushButton,
            Label,
            Calendar,
            ComboBox,
            LineEdit,
            DateEdit,
            Dialog
        ]

        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        font_name = Model().read("settings")[0][2]
        font = QFont(font_name)

        self.lbl_name.setFont(font)
        self.lbl_date.setFont(font)
        self.lbl_status.setFont(font)