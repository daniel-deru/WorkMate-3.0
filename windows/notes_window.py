import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from PyQt5.QtWidgets import QDialog, QWidget

from designs.python.note_window import Ui_Note_Window

from styles.windows.noteWindow import note_window_styles
from utils.message import Message
from database.model import Model



class Note_window(QDialog, Ui_Note_Window):
    def __init__(self):
        super(Note_window, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(note_window_styles)

        self.chkbx_edit.stateChanged.connect(self.editable)
        self.btn_save.clicked.connect(self.save_clicked)

    def editable(self):
        checkbox = self.chkbx_edit
        if checkbox.isChecked():
            self.txtedt_body.setReadOnly(False)
        else:
            self.txtedt_body.setReadOnly(True)

    def save_clicked(self):
        name = self.lnedt_title.text()
        body = self.txtedt_body.toPlainText()
        if not self.lnedt_title.text():
            message = Message("Please enter a title for your note.", "Note")
            message.exec_()
        else:
            note = {
                'name': name,
                'body': body
            }
            Model().save("notes", note)
            print(Model().read("notes"))


    