import sys
import os

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from integrations.onedrive import OneDrive

class OneDriveUpload(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    
    def upload(self):
        onedrive = OneDrive()
        onedrive.upload()
        self.finished.emit(True)
        
    
class OneDriveDownload(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    
    def download(self):
        onedrive = OneDrive()
        onedrive.download()
        self.finished.emit(True)