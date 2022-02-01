import sys
import os

from PyQt5.QtWidgets import QDialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.protected_apps_view_window import Ui_ProtectedView

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet


class ProtectedView(QDialog, Ui_ProtectedView):
    def __init__(self, app):
        super(ProtectedView, self).__init__()
        self.setupUi(self)
        self.read_styles()

    def read_styles(self):
        styles = [
            PushButton,
            Label,
            Dialog
        ]

        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    