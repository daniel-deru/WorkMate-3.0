import os
import sys
import pyperclip

from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QTextCursor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from designs.python.note_window import Ui_Note_Window


from utils.message import Message
from database.model import Model
import assets.resources
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
        self.setWindowIcon(QIcon(":/other/app_icon"))

        self.custom_text_edit = CustomTextEdit().create()
        self.layout().addWidget(self.custom_text_edit)

        self.read_styles()

        self.chkbx_edit.stateChanged.connect(self.set_delete_active)

        self.note = edit_note
        if self.note:
            self.lnedt_title.setText(self.note[1])
            self.custom_text_edit.setPlainText(self.note[2])
            self.btn_save.setText("Update")
            self.text = self.note[2]
        self.btn_save.clicked.connect(self.save_clicked)
        self.btn_copy_note.clicked.connect(self.copy_text)
    
    def set_delete_active(self):
            delete_checked = self.chkbx_edit.isChecked()
            if delete_checked:
                self.custom_text_edit.delete_signal.emit(True)
            elif not delete_checked:
                self.custom_text_edit.delete_signal.emit(False)


    def save_clicked(self):
        name = self.lnedt_title.text()
        body = self.custom_text_edit.toPlainText()
        
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
        body = self.custom_text_edit.toPlainText()
        pyperclip.copy(body)
        pass

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
        self.custom_text_edit.setFont(QFont(font))
        self.btn_copy_note.setFont(QFont(font))
        self.lnedt_title.setFont(QFont(font))



# Custom Text Edit class to get access to the keypress event in order to stop users from deleting content
class CustomTextEdit(QTextEdit):
    # This is a custom signal to check if the textedit is editable
    delete_signal = pyqtSignal(bool)
    def __init__(self):
        super(CustomTextEdit, self).__init__()

        self.delete_active = False

        self.delete_signal.connect(self.set_delete_status)
    
    def set_delete_status(self, signal):
        self.delete_active = signal

    def keyPressEvent(self, event):
        if not self.delete_active:
            if event.key() == Qt.Key_Delete:
                self.set_text(self.toPlainText())
                self.moveCursor(QTextCursor.End)
            elif event.key() == Qt.Key_Backspace:
                self.set_text(self.toPlainText())
        super().keyPressEvent(event)
        
    
    def create(self):
        return self

    def set_text(self, text):
        self.setPlainText(text)
