import sys
import os

from PyQt5.QtCore import QObject, pyqtSignal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from database.model import Model


class BrowserImport(QObject):
    finished: pyqtSignal = pyqtSignal(bool)
    
    def __init__(self, data) -> None:
        super(BrowserImport, self).__init__()
        self.data = data
    
    def save(self):
        for entry in self.data:
            name, account = entry
            Model().save("vault", {'type': "app", 'name': name, 'data': account })
        self.finished.emit(True)