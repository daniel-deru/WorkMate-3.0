import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.note_window import Ui_Note_Window


from utils.message import Message
from database.model import Model
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.TextEdit import TextEdit
from widgetStyles.Dialog import Dialog
from utils.helpers import StyleSheet


class Note_window(QDialog, Ui_Note_Window):
    note_window_signal = pyqtSignal(str)
    def __init__(self, edit_note=None):
        super(Note_window, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon("./assets/WorkMate.ico"))
        self.read_styles()

        self.note = edit_note
        if self.note:
            self.lnedt_title.setText(self.note[1])
            self.txtedt_body.setPlainText(self.note[2])
            self.btn_save.setText("Update")

        self.chkbx_edit.stateChanged.connect(self.editable)
        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_copy_note.clicked.connect(self.copy_text)

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
            make_note = {
                    'name': name,
                    'body': body
                }
            if not self.note:
                Model().save("notes", make_note)
            else:
                Model().update("notes", make_note, self.note[0])
            self.note_window_signal.emit("note saved")
            self.close()

    def copy_text(self):
        body = self.txtedt_body.toPlainText()
        pyperclip.copy(body)

    def read_styles(self):
        styles = [
            PushButton,
            LineEdit,
            CheckBox,
            TextEdit,
            Dialog,
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.chkbx_edit.setFont(QFont(font))
        self.btn_save.setFont(QFont(font))
        self.txtedt_body.setFont(QFont(font))
        self.btn_copy_note.setFont(QFont(font))
        self.lnedt_title.setFont(QFont(font))
    