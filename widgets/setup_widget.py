import sys
import os
import webbrowser

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QVariantAnimation, QEventLoop
from PyQt5.QtGui import QHideEvent, QColor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

class SetupWidget(QWidget):
    next_signal = pyqtSignal(bool)
    def __init__(self, data) -> None:
        super(SetupWidget, self).__init__()
        
        self.message = data[0]
        self.help_link = data[1]
        self.callback = data[2]
        self.step = data[3]
        self.create_ui()
        
        self.no_button.clicked.connect(lambda: self.next_signal.emit(True))
        self.yes_button.clicked.connect(self.run_callback)
        self.btn_help.clicked.connect(lambda: webbrowser.open_new_tab(self.help_link))
        
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
        
        lbl_message: QLabel = QLabel(self.message)
        lbl_message.setAlignment(Qt.AlignCenter)
        lbl_message.setStyleSheet("font-size: 20px;font-weight: bold;")
        
        lbl_step: QLabel = QLabel(self.step)
        lbl_step.setAlignment(Qt.AlignCenter)
        lbl_step.setStyleSheet("font-size: 20px;font-weight: bold;height: 10px;")
        
        self.btn_help = QPushButton("What's This?")
        btn_container = QHBoxLayout()
        btn_container.addWidget(self.help_link)
        
        
        vbox.addWidget(lbl_step)
        vbox.addWidget(lbl_message)
        vbox.addWidget(btn_container)
        vbox.addLayout(hbox_button_container)
        
        self.setLayout(vbox)
        
    def create_widget(self):
        return self
        
        
        
        