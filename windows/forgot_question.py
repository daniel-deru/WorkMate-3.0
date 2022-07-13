import sys
import os

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.forgot_question import Ui_AnswerQuestionDialog

from utils.helpers import StyleSheet

from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.LineEdit import LineEdit
from widgetStyles.Label import Label

from database.model import Model

from windows.reset_password import ResetPassword


class PasswordQuestion(Ui_AnswerQuestionDialog, QDialog):
    def __init__(self):
        super(PasswordQuestion, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        user: list[tuple] = Model().read('user')[0]
        self.correct_phrase: str = user[4]


        self.btn_enter.clicked.connect(self.verify_answer)

    def read_styles(self):
        widgetlist: list[str] = [
            Dialog,
            PushButton,
            LineEdit,
            Label
        ]

        stylesheet: str = StyleSheet(widgetlist).create()
        self.setStyleSheet(stylesheet)
        
        font_name = Model().read("settings")[0][2]
        
        font_widgets = [
            self.lbl_question,
            self.lnedt_answer,
            self.btn_enter
        ]
        
        widget: QWidget
        for widget in font_widgets:
            widget.setFont(QFont(font_name))

    def verify_answer(self):
        answer: str = self.lnedt_answer.text()
        if(answer == self.correct_phrase):
            self.close()
            reset_password_window = ResetPassword()
            reset_password_window.exec_()
        else:
            text: str = self.lbl_question.text()
            self.lbl_question.setText(text + "\nIncorrect Answer")