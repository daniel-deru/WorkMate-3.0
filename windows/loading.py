import sys
import os

from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import QVariantAnimation, pyqtSlot, QVariant, QAbstractAnimation, Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.loading import Ui_LoadingDialog

# https://stackoverflow.com/questions/55258872/how-to-animate-an-image-icon-widget


class Loading(QDialog):
    def __init__(self):
        super(Loading, self).__init__()

        image = Spinner(alignment=Qt.AlignCenter)
        image.start_animation()
        
        vbox = QVBoxLayout()
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
            duration=10*1000,
            valueChanged=self.on_valueChanged
                        
        )
    
    
    @pyqtSlot(QVariant)
    def on_valueChanged(self, value):
        t: QTransform = QTransform()
        t.rotate(value)
        self.setPixmap(self.pixmap.transformed(t))
        
    def start_animation(self):
        if self.animation.state() != QAbstractAnimation.Running:
            self.animation.start()
