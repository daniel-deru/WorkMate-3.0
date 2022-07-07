import sys
import os

from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QVariantAnimation, pyqtSlot, QVariant, QAbstractAnimation, Qt, QSize

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.loading import Ui_LoadingDialog

# https://stackoverflow.com/questions/55258872/how-to-animate-an-image-icon-widget


class Loading(QDialog):
    def __init__(self, message="Loading... Please wait."):
        super(Loading, self).__init__()
        self.setStyleSheet("background-color: black;")
        image = Spinner(alignment=Qt.AlignCenter)
        image.setFixedSize(QSize(400, 200))
        image.setStyleSheet("text-align: center;")
        image.start_animation()
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px;font-weight: 800; color: white;")
        self.label.setFixedWidth(400)
        # QSpacerItem()
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addWidget(image)
        self.setLayout(vbox)
    
        
class Spinner(QLabel):
    def __init__(self, *args, **kwargs):
        super(Spinner, self).__init__(*args, **kwargs)
        self.pixmap = QPixmap(":/other/loader.svg")
        
        self.animation = QVariantAnimation(
            self,
            startValue=0.0,
            endValue=3600.0,
            duration=12*1000,
            valueChanged=self.on_valueChanged
                        
        )
        
        self.animation.setLoopCount(-1)
    
    
    @pyqtSlot(QVariant)
    def on_valueChanged(self, value):
        t: QTransform = QTransform()
        t.rotate(value)
        self.setPixmap(self.pixmap.transformed(t))
        
    def start_animation(self):
        if self.animation.state() != QAbstractAnimation.Running:
            self.animation.start()
