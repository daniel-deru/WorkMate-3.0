import random
import pyperclip
import sys
import os
import math
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QSlider, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QKeyEvent, QMouseEvent

from designs.python.generate_password import Ui_GeneratePasswordWindow
from utils.globals import CHAR_GROUPS

class GeneratePasswordWindow(Ui_GeneratePasswordWindow, QDialog):
    def __init__(self) -> None:
        super(GeneratePasswordWindow, self).__init__()
        self.setupUi(self)
        self.password_length: int = 1
        
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
        
    def generate_password(self):
        character_list = []
        
        for _ , value in self.characters.items():
            should_use, codes = value
            if should_use: character_list.extend(codes)
            
        exclude_codes = self.get_excluding_characters()
        
        excluded_character_list = [x for x in character_list if x not in exclude_codes]

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
        x = 0
        # TODO Test these regex rules
        lower_reg = r"[a-z]+"
        upper_reg = r"[A-Z]+"
        number_reg = r"[0-9]+"
        punctuation = r"[.,:;!?\"'`]+"
        special_char = r"[#$&@~_|]+"
        math_reg = r"[+=-*^/%]+"
        brackets = r"[\{\}\[\]\/\(\)]+"
        
        entropy = math.log2(x**password_length)
        
        
    