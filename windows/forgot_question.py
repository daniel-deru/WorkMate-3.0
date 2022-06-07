import sys
import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

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
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        user: list[tuple] = Model().read('user')[0]
        question: str = user[4]
        self.correct_answer: str = user[5]

        self.lbl_question.setText(question)

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

    def verify_answer(self):
        answer: str = self.lnedt_answer.text()
        if(answer == self.correct_answer):
            self.close()
            reset_password_window = ResetPassword()
            reset_password_window.exec_()
        else:
            text: str = self.lbl_question.text()
            self.lbl_question.setText(text + "\nIncorrect Answer")