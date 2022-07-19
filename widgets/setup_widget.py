import sys
import os

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

class SetupWidget(QWidget):
    next_signal = pyqtSignal(bool)
    def __init__(self, data) -> None:
        super(SetupWidget, self).__init__()
        
        self.message, self.callback = data
        self.create_ui()
        
        self.no_button.clicked.connect(lambda: self.next_signal.emit(True))
        self.yes_button.clicked.connect(self.run_callback)
        
    def run_callback(self):
        self.callback()
        self.next_signal.emit(True)
        
    
    def create_ui(self):
        vbox = QVBoxLayout()
        
        hbox_button_container = QHBoxLayout()
        
        self.yes_button = QPushButton("Yes")
        self.no_button = QPushButton("No")
        
        hbox_button_container.addWidget(self.yes_button)
        hbox_button_container.addWidget(self.no_button)
        
        lbl_message = QLabel(self.message)
        
        vbox.addWidget(lbl_message)
        vbox.addLayout(hbox_button_container)
        
        self.setLayout(vbox)
        
    def create_widget(self):
        return self
        
        
        
        