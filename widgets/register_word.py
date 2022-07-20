import sys
import os
import pyperclip

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model

class RegisterWordButton(QPushButton): 
    
    def __init__(self, data, number=None):
        super(RegisterWordButton, self).__init__()
        self.data = data
        self.clicked.connect(lambda: pyperclip.copy(data))
        font_name = Model().read("settings")[0][2]
        self.setFont(QFont(font_name))
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f"{str(number).zfill(2)}. {data}")
        self.setStyleSheet("""QPushButton {
                                text-align: left;
                                background-color: white;
                                border: 2px solid #9ecd16;
                                color: black;
                            }
                            QPushButton:hover {
                                background-color: #9ecd16;
                                color: white;
                            }
                            QPushButton:pressed {
                                    background-color: white;
                                    color: black;
                            }""")
        
        
    
        
        
        