import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QWidget, QLineEdit, QToolButton, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon



from widgetStyles.Widget import Widget
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton

from utils.helpers import StyleSheet

from database.model import Model

class PasswordWidget(QWidget):
    def __init__(self, input=None):
        super(PasswordWidget, self).__init__()
        
        self.input = input
        night_mode = Model().read("settings")[0][1]
        self.open_icon = ":/input/eye_white_open.svg" if int(night_mode) else ":/input/eye_black_open.svg"
        self.closed_icon = ":/input/eye_white_closed.svg" if int(night_mode) else ":/input/eye_black_closed.svg"
        self.createWidget()
        self.read_styles()
        self.returnWidget()

    def createWidget(self):
        hbox: QHBoxLayout = QHBoxLayout()
        
        

        self.text_field: QLineEdit = QLineEdit()
        self.text_field.setEchoMode(QLineEdit.Password)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text_field.setSizePolicy(sizePolicy)
        
        if(self.input):
            self.text_field.setText(self.input)
        self.show_button: QToolButton = QToolButton()
        
        
        self.show_button.setIcon(QIcon(self.open_icon))
        self.show_button.setCursor(Qt.PointingHandCursor)
        self.show_button.clicked.connect(self.show_hide_password)

        hbox.addWidget(self.text_field)
        hbox.addWidget(self.show_button)

        self.setLayout(hbox)
        self.setMinimumWidth(200)

    def show_hide_password(self):
        if self.text_field.echoMode() == QLineEdit.Password:
            self.text_field.setEchoMode(QLineEdit.Normal)
            self.show_button.setIcon(QIcon(self.closed_icon))
        else:
            self.text_field.setEchoMode(QLineEdit.Password)
            self.show_button.setIcon(QIcon(self.open_icon))

    
    def returnWidget(self):
        return self

    def read_styles(self):
        widget_list = [
            Widget,
            LineEdit,
            ToolButton
        ]
        stylesheet: str = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widgets = [
            self.text_field
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
    