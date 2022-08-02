import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox

class FilterGroupWidget(QWidget):
    def __init__(self) -> None:
        super(FilterGroupWidget, self).__init__()
        self.setupUi()
        
    def setupUi(self):
        hbox = QHBoxLayout()
        
        cmb_groups = QComboBox()
        btn_manage_groups = QPushButton()
        
        hbox.addWidget(cmb_groups)
        hbox.addWidget(btn_manage_groups)
        
        self.setLayout(hbox)