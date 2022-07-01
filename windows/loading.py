import sys
import os

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.loading import Ui_LoaderWidget


class LoadingScreen(Ui_LoaderWidget, QDialog):
    upload_done = pyqtSignal(bool)
    def __init__(self):
        super(LoadingScreen, self).__init__()
        self.setupUi(self)
        
        # self.pixmap: QPixmap = QPixmap(":/other/loader.svg")
        # self.lbl_image.setPixmap(self.pixmap)
        # self.lbl_backup_message.setStyleSheet("font-size: 25px;")
        
    #     th = threading.Thread(target=self.upload_thread, daemon=True)
    #     th.start()
    #     return None
        
        
    
    # async def upload_thread(self):
    #     await Google.upload_backup()
    #     self.upload_done.emit(True)