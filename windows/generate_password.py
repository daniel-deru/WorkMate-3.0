import random
import pyperclip
import sys
import os
import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QSlider, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from designs.python.generate_password import Ui_GeneratePasswordWindow

from utils.globals import CHAR_GROUPS
from utils.helpers import char_in_string, StyleSheet
from utils.message import Message

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog
from widgetStyles.QCheckBox import CheckBox, custom_eye
from widgetStyles.HSlider import HSlider
from widgetStyles.ProgressBar import ProgressBar, custom_color_bar
from widgetStyles.styles import ProgressBar as ProgressBarStyle
from widgetStyles.Frame import PassGenFrame

class GeneratePasswordWindow(Ui_GeneratePasswordWindow, QDialog):
    def __init__(self) -> None:
        super(GeneratePasswordWindow, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.password_length: int = 12
        self.lbl_display_length.setText(str(self.password_length))
        
        self.characters = {
            'uppercase': [False, CHAR_GROUPS.UPPERCASE],
            'lowercase': [False, CHAR_GROUPS.LOWERCASE],
            'numbers': [False, CHAR_GROUPS.NUMBERS],
            'math': [False, CHAR_GROUPS.MATH],
            'punctuation': [False, CHAR_GROUPS.PUNCTUATION],
            'special': [False, CHAR_GROUPS.SPECIAL],
            'brackets': [False, CHAR_GROUPS.BRACKETS]
        }
        
        self.slide_length.valueChanged.connect(self.set_length)
        
        self.chk_uppercase.stateChanged.connect(lambda checked: self.set_char_list(checked, 'uppercase'))
        self.chk_lowercase.stateChanged.connect(lambda checked: self.set_char_list(checked, 'lowercase'))
        self.chk_numbers.stateChanged.connect(lambda checked: self.set_char_list(checked, 'numbers'))
        self.chk_math.stateChanged.connect(lambda checked: self.set_char_list(checked, 'math'))
        self.chk_punctuation.stateChanged.connect(lambda checked: self.set_char_list(checked, 'punctuation'))
        self.chk_special.stateChanged.connect(lambda checked: self.set_char_list(checked, 'special'))
        self.chk_brackets.stateChanged.connect(lambda checked: self.set_char_list(checked, 'brackets'))
        
        f: QLineEdit = self.lne_password
        p: QLineEdit = QLineEdit.Password
        n: QLineEdit = QLineEdit.Normal
        self.chk_show.stateChanged.connect(lambda s: f.setEchoMode(p) if s else f.setEchoMode(n))
        
        self.btn_copy.clicked.connect(lambda: pyperclip.copy(self.lne_password.text()))
        
        self.btn_generate.clicked.connect(self.generate_password)
        
        self.lne_password.textChanged.connect(self.calc_entropy)
        
    def read_styles(self):
        widget_list = [
            Dialog,
            PushButton,
            Label,
            LineEdit,
            custom_eye("#chk_show"),
            CheckBox,
            HSlider,
            ProgressBar,
            PassGenFrame("#frame_checkbox_container")
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
    def generate_password(self):
        character_list = []
        
        for _ , value in self.characters.items():
            should_use, codes = value
            if should_use: character_list.extend(codes)
            
        exclude_codes = self.get_excluding_characters()
        
        excluded_character_list = [x for x in character_list if x not in exclude_codes]
        
        if len(character_list) < 1:
            Message("Please choose which characters you want to use.", "Invalid character range").exec_()
            return

        password_codes = random.choices(excluded_character_list, k=self.password_length)
        password = ''
        for code in password_codes:
            password += chr(code)
            
        self.lne_password.setText(password)
        
        
    def set_char_list(self, checked, key):
        self.characters[key][0] = True if checked else False
    
    def set_length(self, value):  
        self.password_length = value
        self.lbl_display_length.setText(str(value))
        
    def get_excluding_characters(self):
        exclude_string: list[str] = list(self.lne_exclude.text())
        exclude_codes = list(map(lambda char: ord(char), exclude_string))
        return exclude_codes
    
    def calc_entropy(self, password):
        password_length = len(self.lne_password.text())
        pool_size = 0
        
        # Check for lowercase
        if char_in_string(password, r"[a-z]+"): pool_size += 26
        
        # Check for uppercase
        if char_in_string(password, r"[A-Z]+"): pool_size += 26
        
        # Check for numbers
        if char_in_string(password, r"\d+"): pool_size += 10
        
        # Check for punctuation
        if char_in_string(password, r"[.,:;!?\"'`]+"): pool_size += 9
        
        # Check for special chars
        if char_in_string(password, r"[#$&@~_|]+"): pool_size += 7
        
        # Check for math symbols
        if char_in_string(password, r"[\+\=\-*^/%]+"): pool_size += 7
        
        # Check for brackets
        if char_in_string(password, r"[{}\[\]()<>]+"): pool_size += 8      
        
        entropy = math.log2(pool_size**password_length)
        
        self.set_password_strength(entropy)

    def set_password_strength(self, strength):
        password_strength: str = ""
        color = ProgressBarStyle.red
        
        if strength < 40:
            password_strength = "Horrible"
            color = ProgressBarStyle.red
        if strength > 40 and strength <= 65:
            password_strength = "Weak"
            color = ProgressBarStyle.orange
        if strength > 65 and strength < 100:
            password_strength = "Good"
            color = ProgressBarStyle.yellow
        if strength > 100:
            password_strength = "Strong"
            color = ProgressBarStyle.green
        
        self.bar_strength.setFormat(password_strength)
        
        if strength > 150: strength = 150
        self.bar_strength.setValue(int(strength))
        
        
        self.bar_strength.setStyleSheet(custom_color_bar(color))
               

        
        
    