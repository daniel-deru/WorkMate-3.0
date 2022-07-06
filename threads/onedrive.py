import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message

from workers.onedrive_worker import OneDriveUpload, OneDriveDownload

from windows.loading import Loading


def upload_onedrive(self, show_message=True):
        
    # Create Google upload thread and google upload worker
    self.upload_onedrive_thread = QThread()  
    self.onedrive_upload_worker = OneDriveUpload()
    
    # Move the worker process to the thread
    self.onedrive_upload_worker.moveToThread(self.upload_onedrive_thread)
    
    # signal to start the worker code when the thread starts
    self.upload_google_thread.started.connect(self.onedrive_upload_worker.upload)
    
    # Close the loading screen after the worker thread is done
    self.onedrive_onedrive_worker.finished.connect(lambda: self.onedrive_upload_loading.close())
    
    # Clean up the thread and worker
    self.onedrive_upload_worker.finished.connect(self.onedrive_upload_worker.deleteLater)
    self.upload_onedrive_thread.finished.connect(self.upload_onedrive_thread.deleteLater)
    
    self.upload_onedrive_thread.start()
    
    # Show loading screen while worker is busy
    self.onedrive_upload_loading = Loading()
    self.onedrive_upload_loading.exec_()
    
    if show_message:
        message: Message = Message("The backup is complete", "Backup Successful")
        message.exec_()