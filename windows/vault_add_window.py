from dataclasses import field
from email.charset import QP
import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog,QHBoxLayout, QLineEdit, QPushButton


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_add_window import Ui_AddSecret_window

from widgetStyles.PushButton import PushButton
from widgetStyles.SpinBox import SpinBox
from widgetStyles.Label import Label
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet


class AddSecret(QDialog, Ui_AddSecret_window):
    def __init__(self):
        super(AddSecret, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.columns = 0

        self.lnedt_columns.textChanged.connect(self.make_columns)

    def make_columns(self):
        columns = self.lnedt_columns.text()
        fields_container = self.vbox_column_def
        for i in range(fields_container.count() - 1):
            fields_container.layout().itemAt(i).widget().deleteLater()
        print(fields_container.count())
        if columns.isnumeric():
            if int(columns) <= 5:
                self.create_fields(int(columns))

    def read_styles(self):
        styles = [
            PushButton,
            SpinBox,
            Label,
            LineEdit,
            Dialog
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def create_fields(self, columns):
        for i in range(columns):
            # field_box = QHBoxLayout()
            # field_box.setObjectName(f"{i}")

            # field_line = QLineEdit()
            # data_line = QLineEdit()

            # field_box.addWidget(field_line)
            # field_box.addWidget(data_line)
            field_box = QPushButton(f"{i}")

            self.vbox_column_def.addWidget(field_box)