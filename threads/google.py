import sys
import os

from PyQt5.QtCore import QThread

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.message import Message

from workers.google_drive_worker import GoogleUpload

from windows.loading import Loading

# Method to create Thread for uploading to Google Drive
def upload_google(self):
    
    # Create Google upload thread and google upload worker
    self.upload_google_thread = QThread()  
    self.google_upload_worker = GoogleUpload()
    
    # Move the worker process to the thread
    self.google_upload_worker.moveToThread(self.upload_google_thread)
    
    # signal to start the worker code when the thread starts
    self.upload_google_thread.started.connect(self.google_upload_worker.upload)
    
    # Close the loading screen after the worker thread is done
    self.google_upload_worker.finished.connect(lambda: self.google_upload_loading.close())
    
    # Clean up the thread and worker
    self.google_upload_worker.finished.connect(self.google_upload_worker.deleteLater)
    self.upload_google_thread.finished.connect(self.upload_google_thread.deleteLater)
    
    self.upload_google_thread.start()
    
    # Show loading screen while worker is busy
    self.google_upload_loading = Loading()
    self.google_upload_loading.exec_()
    
    message: Message = Message("The backup is complete", "Backup Successful")
    message.exec_()