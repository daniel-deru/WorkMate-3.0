import sys
import os
import pyperclip
import math
from datetime import date, timedelta

from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QWidget, QGraphicsBlurEffect, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QSize, pyqtSlot

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.register_window import Ui_Register
from utils.message import Message
from database.model import Model
from utils.helpers import StyleSheet, random_words
from windows.passphase_copy_window import PassphraseCopyWindow

import assets.resources

from widgets.register_word import RegisterWordButton

from widgetStyles.PushButton import PushButton, IconToolButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.Widget import SideWidget
from widgetStyles.QCheckBox import BlackEyeCheckBox
from widgetStyles.Calendar import Calendar
from widgetStyles.DateEdit import DateEditForm

from utils.message import Message

from windows.generate_password import GeneratePasswordWindow

class Register(Ui_Register, QDialog):
    register_close_signal = pyqtSignal(str)
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        
        self.passphrase_safe = False
        self.dte_password_exp.setDate(date.today() + timedelta(days=90))
        
        pixmap = QPixmap(":/other/SMT Logo.png")
        app_logo_pixmap = QPixmap(":/other/app_logo")
        app_logo_pixmap = app_logo_pixmap.scaledToWidth(200)
        self.lbl_company.setPixmap(pixmap)
        self.lbl_workmate_logo.setPixmap(app_logo_pixmap)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.lnedt_password.setEchoMode(QLineEdit.Password)
        self.lnedt_password2.setEchoMode(QLineEdit.Password)
        
        words = self.set_random_words()
        self.read_styles()
        
        self.btn_register.clicked.connect(self.register_clicked)
        self.btn_copy.clicked.connect(lambda: pyperclip.copy(words))
        self.tbtn_generate_password.clicked.connect(self.generate_password)
        
        self.chk_password.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password, self.chk_password))
        self.chk_password2.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password2, self.chk_password2))
        
        self.registered = False
        
        word_widget: QWidget = self.word_widget
        word_widget.setAttribute(Qt.WA_Hover, True)
        
        word_widget.enterEvent = self.mouseHover
        word_widget.leaveEvent = self.mouseLeave
        
        self.set_blur()
        
    
    @pyqtSlot()
    def generate_password(self):
        GeneratePasswordWindow().exec_()
        

    def register_clicked(self):
        name = self.lnedt_name.text()
        email = self.lnedt_email.text()
        password1 = self.lnedt_password.text()
        password2 = self.lnedt_password2.text()
        password_exp = self.dte_password_exp.date().toPyDate()

        fields = [
            name,
            email,
            password1,
            password2,
        ]

        valid_submition = False
        
        for field in fields:
            if not field:
                Message(f"Make sure you fill in all the fields.", "Please fill in all the fields").exec_()
                break
            else:
                valid_submition = True

        if password1 != password2:
            Message("Please make sure your passwords match. Check to see if your caps lock is on", "Passwords don't match").exec_()
        elif valid_submition:
            data = {
                "name": name,
                "email": email,
                "password": password1,
                "passphrase": self.words,
                "password_exp": password_exp
            }
            
            message = PassphraseCopyWindow()
            message.yes_signal.connect(self.set_passphrase_safe)
            message.exec_()
            
            if not self.passphrase_safe: return

            Model().save("user", data)
            self.registered = True
            self.register_close_signal.emit("user created")
            self.close()
    
    def set_passphrase_safe(self, response):
        self.passphrase_safe = response

    def read_styles(self):
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog,
            SideWidget,
            BlackEyeCheckBox,
            DateEditForm,
            Calendar,
            IconToolButton()
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        self.lbl_create_account.setStyleSheet("color: white;margin-top: 30px;font-size: 20px;font-weight: 700;height: 200px;")
        self.lbl_developed_by.setStyleSheet("color: white;")
        self.lbl_passphrase_desc.setStyleSheet("font-weight: 700;")
        
        font_name = Model().read("settings")[0][2]
        
        self.tbtn_generate_password.setIcon(QIcon(":/button_icons/password"))
        self.tbtn_generate_password.setIconSize(QSize(30, 20))
        
        font_widgets = [
            self.lbl_company,           self.lbl_create_account,
            self.lbl_developed_by,      self.lbl_email,
            self.lbl_name,              self.lbl_passphrase_desc,
            self.lbl_password,          self.lbl_password2,
            self.lbl_warning,           self.lnedt_email,
            self.lnedt_name,            self.lnedt_password,
            self.lnedt_password2,       self.btn_copy,
            self.btn_register,          self.lbl_generate_password,
            self.lbl_password_exp,      self.dte_password_exp
        ]
        
        widget: QWidget
        
        for widget in font_widgets:
            widget.setFont(QFont(font_name))
        
        

    def closeEvent(self, event):
        if not self.registered:
            self.register_close_signal.emit("window closed")
        elif self.registered:
            self.register_close_signal.emit("registered")
            
    def set_random_words(self):
        random: list[str] = random_words()
        string: str = " ".join(random)
        container: QGridLayout = self.gbox_words
        
        count = 1
        for i in range(math.floor(len(random)/4)):
            for j in range(4):
                button: RegisterWordButton = RegisterWordButton(random[count - 1], count)                
                container.addWidget(button, i, j)
                count += 1
                
        self.words = string
        return string
    
    def show_hide_password(self, line_edit, checkbox):
        if checkbox.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)
                    
    def mouseHover(self, event):
        blur: QGraphicsBlurEffect = QGraphicsBlurEffect()
        blur.setBlurRadius(0)
        word_widget: QWidget = self.word_widget      
        word_widget.setGraphicsEffect(blur)
        
    def mouseLeave(self, event):
        self.set_blur()
        
    def set_blur(self):
        blur: QGraphicsBlurEffect = QGraphicsBlurEffect()
        blur.setBlurRadius(10)
        word_widget: QWidget = self.word_widget
        word_widget.setGraphicsEffect(blur)
    
    def copy_word(self, some):
        # print(some)
        pass


