import sys
import os
import re
import math
from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QLabel, QLineEdit, QWidget

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.crypto_vault_window import Ui_CryptoVault

from widgetStyles.Dialog import Dialog
from widgetStyles.ComboBox import ComboBox
from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit

from utils.helpers import StyleSheet, clear_window

class CryptoVaultWindow(Ui_CryptoVault, QDialog):
    def __init__(self):
        super(CryptoVaultWindow, self).__init__()
        self.setupUi(self)
        self.displayWordBoxes()
        self.read_styles()

        self.cmb_num_words.currentIndexChanged.connect(self.update)

    def read_styles(self):
        widget_list = [
            Dialog,
            ComboBox,
            Label,
            PushButton,
            LineEdit
        ]
        self.setMinimumHeight(600)
        stylesheet = StyleSheet(widget_list).create()

        self.setStyleSheet(stylesheet)

    def displayWordBoxes(self):
        num_words: str = self.cmb_num_words.currentText()
        # Get the start and end index matching the regex 
        (start, end) = re.match("^\d+", num_words).span()
        # Get the number of words that needs to be represented
        words: int = int(num_words[start: end])
        grid_items = []

        COLUMNS = 3
        count = 1
        for i in range(math.ceil(words/COLUMNS)):
            subarr = []
            print(i)
            for j in range(COLUMNS):
                hbox = QHBoxLayout()
                widget = QWidget()
                widget.setMinimumWidth(300)

                number = QLabel(f"{str(count).zfill(2)}. ")
                field = QLineEdit()

                widget.setLayout(hbox)

                hbox.addWidget(number)
                hbox.addWidget(field)

                if(count > words):
                    break
                button = QPushButton(f"Button {count}")
                self.gbox_words.addWidget(widget, i, j)
                count += 1

        

    def update(self):
        clear_window(self.gbox_words)
        self.displayWordBoxes()
        self.read_styles()