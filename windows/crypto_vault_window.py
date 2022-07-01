import sys
import os
import re
import math
from typing import Match, Pattern
from json import dumps, loads
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QWidget, QGridLayout, QComboBox
from PyQt5.QtCore import pyqtSignal
from pyparsing import line

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.crypto_vault_window import Ui_CryptoVault

from widgetStyles.Dialog import Dialog
from widgetStyles.ComboBox import ComboBox
from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.ToolButton import ToolButton
from widgetStyles.QCheckBox import WhiteEyeCheckBox, BlackEyeCheckBox

from utils.helpers import StyleSheet, clear_window
from utils.message import Message

from widgets.password_show_hide import PasswordWidget

from database.model import Model

class CryptoVaultWindow(Ui_CryptoVault, QDialog):
    crypto_update_signal = pyqtSignal(bool)
    def __init__(self, secret=None):
        super(CryptoVaultWindow, self).__init__()
        self.secret: tuple or None = secret
        
        self.setupUi(self)
        self.displayWordBoxes()
        self.read_styles()
        if self.secret: self.fill_data()


        self.cmb_num_words.currentIndexChanged.connect(self.update)
        self.chk_password1.stateChanged.connect(lambda: self.show_hide_password(self.chk_password1, self.lne_password1))
        self.chk_password2.stateChanged.connect(lambda: self.show_hide_password(self.chk_password2, self.lne_password2))
        self.chk_private_key.stateChanged.connect(lambda: self.show_hide_password(self.chk_private_key, self.lne_private))
        self.btn_save.clicked.connect(self.save)

    def read_styles(self):
        night_mode_on = Model().read("settings")[0][1]
        checkbox = WhiteEyeCheckBox if night_mode_on else BlackEyeCheckBox
        widget_list = [
            checkbox,
            Dialog,
            ComboBox,
            Label,
            PushButton,
            LineEdit,
            ToolButton
        ]
        self.setMinimumHeight(850)
        stylesheet = StyleSheet(widget_list).create()

        self.setStyleSheet(stylesheet)

    def displayWordBoxes(self):        
        words: int = self.get_num_words()

        COLUMNS: int = 3
        count: int = 1
        existing_words: None = None
        if(self.secret):
            data: object = self.get_data()
            existing_words: list[str] = data['words'].split(" ")
            if words > len(existing_words):
                existing_words += ["" for _ in range(words - len(existing_words))]

        for i in range(math.ceil(words/COLUMNS)):
            for j in range(COLUMNS):
                hbox: QHBoxLayout = QHBoxLayout()
                hbox.setContentsMargins(0, 0, 0, 0)
                widget: QWidget = QWidget()

                number: QLabel = QLabel(f"{str(count).zfill(2)}. ")
                param = existing_words[count-1] if existing_words else None
                password: PasswordWidget = PasswordWidget(param)

                hbox.addWidget(number)
                hbox.addWidget(password)

                widget.setLayout(hbox)

                if(count > words):
                    break
                self.gbox_words.addWidget(widget, i, j)
                
                count += 1
        
        

    def update(self) -> None:
        clear_window(self.gbox_words)
        self.displayWordBoxes()
        self.read_styles()

    def save(self) -> None:
        password1: str = self.lne_password1.text()
        password2: str = self.lne_password2.text()

        description:str = self.lne_description.text()
        username: str = self.lne_name.text()
        num_words: int = self.get_num_words()
        words_layout: QGridLayout = self.gbox_words
        words: list[str] = []
        
        public_key: str = self.lne_public.text()
        private_key: str = self.lne_private.text()

        valid_submit: bool = True

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

        if(password1 and (password1 != password2)):
            Message("The passwords don't match", "Passwords Incorrect").exec_()
            valid_submit = False

        if(not description): 
            valid_submit = False
            Message("Please Provide a description", "No Description").exec_()
        if(not username): 
            valid_submit = False
            Message("Please Provide a username", "No Username").exec_()
        

        num_words = self.get_num_words()
        if(len(words) < num_words):
            Message(f"You have {len(words)} words but, you need {num_words} words. Please check for missing fields", "Missing Words").exec_()
            valid_submit = False

        
        if(valid_submit):
            data = {
                'name': username,
                'num_words': num_words,
                'words': " ".join(words),
                'description': description,
                'password': password1
            }
            
            
            if private_key:
                data['private_key'] = private_key
            if public_key:
                data['public_key'] = public_key
                
            data: str = dumps(data)

            if self.secret:
                Model().update("vault", {'type': 'crypto', 'name': description, 'data':data}, self.secret[0])
            else:
                Model().save("vault", {'type': 'crypto', 'name': description, 'data': data})

            self.crypto_update_signal.emit(True)
            self.close()
    
    def get_num_words(self) -> int:
        num_words: str = self.cmb_num_words.currentText()
        # Get the start and end index matching the regex 
        (start, end) = re.match("^\d+", num_words).span()
        # Get the number of words that needs to be represented
        words: int = int(num_words[start: end])

        return words

    def fill_data(self):
        data: object = self.get_data()
        self.lne_description.setText(data['description'])
        self.lne_password1.setText(data['password'])
        self.lne_password2.setText(data['password'])
        self.lne_name.setText(data['name'])
        
        if 'private_key' in data:
            self.lne_private.setText(data['private_key'])
            
        if 'public_key' in data:
            self.lne_public.setText(data['public_key'])

        combobox: QComboBox = self.cmb_num_words

        # Regex to find the correct option in the drop down
        regex: Pattern[str] = f"^{str(data['num_words'])}"

        # Find and set the correct option in the drop down
        for i in range(combobox.count()):
            if(re.match(regex, combobox.itemText(i))):
                combobox.setCurrentIndex(i)
        self.update()
    
    def get_data(self) -> object:
        data: object = loads(self.secret[3])
        return data
    
    def show_hide_password(self, checkbox, line_edit):
        if checkbox.isChecked():
            line_edit.setEchoMode(QLineEdit.Normal)
        else:
            line_edit.setEchoMode(QLineEdit.Password)