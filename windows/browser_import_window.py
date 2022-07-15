import sys
import os

from PyQt5.QtWidgets import QDialog


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.browser_import_window import Ui_BrowserPasswordImportWindow

from widgetStyles.Label import Label


class BrowserImportWindow(Ui_BrowserPasswordImportWindow, QDialog):
    
    def __init__(self) -> None:
        super(BrowserImportWindow, self).__init__()
        self.setupUi(self)