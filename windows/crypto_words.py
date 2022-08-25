import sys
import os
from tkinter.ttk import Style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import math

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QWidget, QLabel, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from designs.python.crypto_words import Ui_CryptoWords

from database.model import Model

from widgets.password_show_hide import PasswordWidget

from utils.message import Message

from utils.helpers import set_font, StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label

class CryptoWords(Ui_CryptoWords, QDialog):
    filled_words: pyqtSignal = pyqtSignal(list)
    def __init__(self, num_words: int, words = None) -> None:
        super(CryptoWords, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.set_style()
        
        self.num_words = num_words
        self.words = words
        
        self.displayWordBoxes()
        
        self.btn_save.clicked.connect(self.save)
        
    def set_style(self):
        styles = [
            PushButton,
            Dialog,
            Label
        ]
        
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        set_font([self.btn_save])
        
    def save(self):
        words_layout: QGridLayout = self.gbox_words
        words: list[str] = []
        
        valid_submit = True
        
        for i in range(words_layout.count()):
            widget_container: QWidget = words_layout.itemAt(i).widget()
            password_widget: QWidget = widget_container.layout().itemAt(1).widget()

            
            line_edit: QLineEdit = password_widget.layout().itemAt(0).widget()

            if(type(line_edit) == QLineEdit):
                word: str = line_edit.text()
                # if(not word):
                    # Message(f"There is no word in block {i + 1}.", "Missing Word").exec_()
                    # valid_submit = False
                if word: words.append(word)
                
        if(len(words) < self.num_words):
            Message(f"You have {len(words)} words but, you need {self.num_words} words. Please check for missing fields", "Missing Words").exec_()
            valid_submit = False
            
        if(valid_submit):
            self.filled_words.emit(words)
            self.close()
        
    def displayWordBoxes(self):        
        COLUMNS: int = 3
        count: int = 1     
        font_name = Model().read("settings")[0][2]

        for i in range(math.ceil(self.num_words/COLUMNS)):
            for j in range(COLUMNS):
                hbox: QHBoxLayout = QHBoxLayout()
                hbox.setContentsMargins(0, 0, 0, 0)
                widget: QWidget = QWidget()
                widget.setContentsMargins(0, 0, 0, 0)

                self.number: QLabel = QLabel(f"{str(count).zfill(2)}. ")
                self.number.setFont(QFont(font_name))
                self.number.setMaximumWidth(30)
                
                param = self.words[count-1] if self.words else None
                password: PasswordWidget = PasswordWidget(param)

                hbox.addWidget(self.number)
                hbox.addWidget(password)

                widget.setLayout(hbox)

                if(count > self.num_words):
                    break
                self.gbox_words.addWidget(widget, i, j)
                
                count += 1