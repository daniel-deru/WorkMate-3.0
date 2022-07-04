import sys
import os

from PyQt5.QtWidgets import QDialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.loading import Ui_LoadingDialog


class Loading(Ui_LoadingDialog, QDialog):
    def __init__(self):
        super(Loading, self).__init__()
        self.setupUi(self)