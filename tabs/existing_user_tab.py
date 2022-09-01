import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import math

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon, QFont

from designs.python.existing_user_tab import Ui_ExistingUser

from utils.helpers import set_font, StyleSheet
from utils.message import Message
from utils.globals import FONT_NAME, DESKTOP

from widgetStyles.Label import Label

from database.model import Model
from database.tables import TableEnum

class ExistingUserTab(Ui_ExistingUser, QWidget):
    def __init__(self) -> None:
        super(ExistingUserTab, self).__init__()
        self.setupUi(self)
        self.set_style()
        self.create_key_inputs()
        
        self.tbtn_database.setIcon(QIcon(":/button_icons/database"))
        
        self.btn_create.clicked.connect(self.submit)
        self.tbtn_database.clicked.connect(self.get_db_path)
        
        
    def submit(self):
        db_path = self.lne_database.text()
        name = self.lne_name.text()
        email = self.lne_email.text()
        words = self.get_words()
        
        verified, message = self.verify_data([db_path, name, email, words])

        if(not verified):
            return Message(message, "Invalid Data")
        
        print("Yay your verified")
        
    def verify_data(self, data: list[str]) -> tuple[bool, str or None]:
        db_path, name, email, words = data
        
        model = Model(db_path)
        user = model.read('user')[0]
        
        db_name = user[1]
        db_email = user[2]
        db_words = user[4]
        
        if(name != db_name):
            return [False, "Invalid Name"]
        elif(email != db_email):
            return [False, "Invalid Email"]
        elif(words != db_words):
            return [False, "Invalid Keys"]
    
        return [True, None]
        
    def get_db_path(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, f"Database File (*.db)")[0]
        self.lne_database.setText(file)

    def get_words(self):
        gbox_item_count = self.gbox_keys.count()
        words = []
        for i in range(gbox_item_count):
            container = self.gbox_keys.layout().itemAt(i)
            lne_key = container.layout().itemAt(1).widget()
            words.append(lne_key.text())
        
        return " ".join(words)
        
    def create_key_inputs(self):
        keys_num: int = 12
        cols: int = 4
        count = 1
        font = QFont(FONT_NAME)
        
        for i in range(math.ceil(keys_num/cols)):
            for j in range(cols):
                hbox = QHBoxLayout()
                lbl_num = QLabel(f"{str(count).zfill(2)}.")
                lne_key = QLineEdit()
                
                lbl_num.setFont(font)
                lne_key.setFont(font)
                
                hbox.addWidget(lbl_num)
                hbox.addWidget(lne_key)
                self.gbox_keys.addLayout(hbox, i, j)
                count += 1 
        
    def create_tab(self):
        return self
    
    def set_style(self):
        style_list = [
            Label
        ]
        
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.lbl_database,
            self.lbl_keys,
            self.lne_database,
            self.btn_create,
            self.lbl_email,
            self.lbl_name,
            self.lne_email,
            self.lne_name
        ]
        
        set_font(widget_list)