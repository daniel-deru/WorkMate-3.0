import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog

from designs.python.app_window import Ui_App_Window

from styles.windows.appWindow import app_window_styles

class Apps_window(QDialog, Ui_App_Window):
    def __init__(self):
        super(Apps_window, self).__init__()
        self.setupUi(self)
        self.setStyleSheet(app_window_styles)