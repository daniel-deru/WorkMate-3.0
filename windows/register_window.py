from ast import arg
import sys
import os
import pyperclip
import math

from PyQt5.QtWidgets import QDialog, QLineEdit, QGridLayout, QHBoxLayout, QWidget, QLabel, QGraphicsBlurEffect, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.register_window import Ui_Register
from utils.message import Message
from database.model import Model
from utils.helpers import StyleSheet, random_words
import assets.resources

from widgets.register_word import RegisterWordButton

from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog
from widgetStyles.Widget import SideWidget
from widgetStyles.QCheckBox import BlackEyeCheckBox

class Register(QDialog, Ui_Register):
    register_close_signal = pyqtSignal(str)
    def __init__(self):
        super(Register, self).__init__()
        self.setupUi(self)
        
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
        self.chk_password.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password, self.chk_password))
        self.chk_password2.stateChanged.connect(lambda: self.show_hide_password(self.lnedt_password2, self.chk_password2))
        
        self.registered = False
        
        word_widget: QWidget = self.word_widget
        word_widget.setAttribute(Qt.WA_Hover, True)
        
        word_widget.enterEvent = self.mouseHover
        word_widget.leaveEvent = self.mouseLeave
        
        self.set_blur()
        
        

    def register_clicked(self):
        name = self.lnedt_name.text()
        email = self.lnedt_email.text()
        password1 = self.lnedt_password.text()
        password2 = self.lnedt_password2.text()
        # question = self.lnedt_question.text()
        # answer = self.lnedt_answer.text()

        fields = [
            name,
            email,
            password1,
            password2,
            # question,
            # answer
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
                "passphrase": self.words
            }

            Model().save("user", data)
            self.registered = True
            self.close()
            self.register_close_signal.emit("user created")

    def read_styles(self):
        styles = [
            PushButton,
            Label,
            LineEdit,
            Dialog,
            SideWidget,
            BlackEyeCheckBox
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        self.lbl_create_account.setStyleSheet("color: white;margin-top: 30px;font-size: 20px;font-weight: 700;height: 200px;")
        self.lbl_developed_by.setStyleSheet("color: white;")
        self.lbl_passphrase_desc.setStyleSheet("font-weight: 700;")
        

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
                # button: QPushButton = QPushButton()
                # button.setStyleSheet("""QPushButton {
                #                             text-align: left;
                #                             background-color: white;
                #                             border: 2px solid #9ecd16;
                #                             color: black;
                #                         }
                #                         QPushButton:hover {
                #                             background-color: #9ecd16;
                #                             color: white;
                #                         }
                #                         QPushButton:pressed {
                #                              background-color: white;
                #                              color: black;
                #                         }""")

                # button.setCursor(Qt.PointingHandCursor)
                # button.clicked.connect(lambda: self.copy_word(count))
                # button.setText(f"{str(count).zfill(2)}. {random[count - 1]}")
                
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
        print(some)


