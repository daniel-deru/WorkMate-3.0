import sys
import os
import threading
import shutil
import json

from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt, QThread
from PyQt5.QtGui import QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton, ButtonFullWidth
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox
from widgetStyles.ScrollBar import ScrollBar

from utils.message import Message
from utils.helpers import StyleSheet
from utils.globals import DB_PATH

from database.model import Model


from windows.forgot_question import PasswordQuestion
from windows.drive_window import DriveWindow
from windows.twofa_window import TwofaDialog
from windows.loading import Loading

from workers.google_drive_worker import GoogleDownload, GoogleUpload

from threads.google import upload_google

from integrations.calendar.c import Google


DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))


class SettingsTab(QWidget, Ui_Settings_tab):
    settings_signal = pyqtSignal(str)
    # This signal will communicate with the main window to get and set the login status
    login_signal = pyqtSignal(str)
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.logged_in = False
        settings = Model().read('settings')[0]
        # Set the default value of the settings
        self.chkbox_nightmode.setChecked(int(settings[1]))
        self.chkbox_calendar.setChecked(int(settings[6]))
        self.chkbox_2fa.setChecked(int(settings[7]))
        
        auto_save_on = json.loads(settings[8])['auto_save']
        self.chk_auto_save.setChecked(auto_save_on)


        # checkbox signals        
        self.chkbox_nightmode.stateChanged.connect(self.set_night_mode)
        self.chkbox_2fa.stateChanged.connect(self.twofa)
        self.chkbox_calendar.stateChanged.connect(self.calendar_toggle)
        self.chk_auto_save.stateChanged.connect(self.auto_save)
        
        self.btn_login.clicked.connect(self.login_clicked)
        self.btn_forgot_password.clicked.connect(self.forgot_password_clicked)
        self.btn_google_drive_sync.clicked.connect(self.restore_from_remote)
        self.btn_save_google_drive.clicked.connect(self.save_to_remote_storage)
        self.btn_save_local.clicked.connect(self.save_local)
        self.btn_restore_local.clicked.connect(self.restore_from_local)
        
        

        # connect the custom signals to the slots
        self.settings_signal.connect(self.read_styles)
        self.login_signal.connect(self.login)

    
    def create_tab(self):
        return self

    # color is at index 3 and nightmode is at index 1
    def set_night_mode(self):
        toggle = self.chkbox_nightmode

        if toggle.isChecked():
            Model().update("settings", {'nightmode': "1"}, 'settings')
            self.settings_signal.emit("settings changed")
            self.updateWindow()
        elif not toggle.isChecked():
            Model().update("settings", {'nightmode': "0"}, 'settings')
            self.settings_signal.emit("settings changed")
            self.updateWindow()
    
    # 2fa slot
    def twofa(self):
        toggle = self.chkbox_2fa
        if(toggle.isChecked()):
            Model().update("settings", {'twofa': '1'}, 'settings')
            twofa_window = TwofaDialog()
            twofa_window.exec_()
        else:
            Model().update('user', {'twofa_key': None}, 'user')
            Model().update("settings", {'twofa': '0'}, 'settings')
    
    def updateWindow(self):
        self.read_styles()
        self.settings_signal.emit("settings")

    def read_styles(self):
        styles = [Label, ButtonFullWidth, SettingsCheckBox, ComboBox, ScrollBar]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
    
    def login(self, signal):
        if signal == "success":
            self.logged_in = True
    
    def check_login(self, signal):
        if signal == "logged in":
            self.logged_in = True
        elif signal == "logged out":
            self.logged_in = False

    def calendar_toggle(self):
        toggle = self.chkbox_calendar
        if toggle.isChecked():
            th = threading.Thread(target=google_thread, daemon=True)
            th.start()
            Model().update("settings", {"calendar": "1"}, "settings")
        elif not toggle.isChecked():
            Model().update("settings", {"calendar": "0"}, "settings")

    def login_clicked(self):
        if self.logged_in:
            self.login_signal.emit("logout requested")
        elif not self.logged_in:
            self.login_signal.emit("login requested")


    def login(self, signal):
        if signal == "logged in":
            self.btn_login.setText("Logout")
            self.logged_in = True
        elif signal == "logged out":
            self.btn_login.setText("login")
            self.logged_in = False

    def forgot_password_clicked(self):
        ask_question = PasswordQuestion()
        ask_question.exec_()
        
    def download_google(self):
        
        # Create a new thread
        self.google_download_thread = QThread()
        
        # Create instance of worker
        self.google_download_worker = GoogleDownload()
        
        # Move the worker to the new thread
        self.google_download_worker.moveToThread(self.google_download_thread)
        
        # Connect thread started signal to worker to start worker when thread is started
        self.google_download_thread.started.connect(self.google_download_worker.download)
        
        # Connect worker finished signal to slot for processing after worker is done
        self.google_download_worker.finished.connect(self.update_db)
        
        # Clean up the processes for better memory management
        self.google_download_worker.finished.connect(self.google_download_worker.deleteLater)
        self.google_download_thread.finished.connect(self.google_download_thread.deleteLater)
        
        self.google_download_thread.start()
        
        self.loading = Loading()
        self.loading.exec_()
        
        message: Message = Message("The restore is complete", "Restore Successful")
        message.exec_()
        
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

    # Slot for the btn_save_google_drive Signal to save to remote storage manually
    def save_to_remote_storage(self):     
        drive_window: DriveWindow = DriveWindow()
        drive_window.drive_dict.connect(self.manual_remote_save)
        drive_window.exec_()

        
    def update_db(self, name: str):
        if Model().is_valid(name):
            os.replace(name, f"{DB_PATH}test.db")
        else:
            message: Message = Message("Your data on the cloud was corrupted. The data did not sync to your local database. Please save a new working backup to your remote storage to prevent data loss", "Sync Failed")
            message.exec_()
        self.loading.close()
        
    def save_local(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path: shutil.copy(f"{DB_PATH}test.db", f"{path}/test.db")
        
    def restore_from_remote(self):
        self.drive_window: DriveWindow = DriveWindow()
        self.drive_window.drive_dict.connect(self.manual_remote_download)
        self.drive_window.exec_()
        
    def restore_from_local(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, "DB File (test.db)")[0]
        
        if not file: return
        
        if Model().is_valid(file):
            shutil.copy(file, f"{DB_PATH}test.db")
        else:
            message: Message = Message("Your data on the cloud was corrupted. The data did not sync to your local database. Please save a new working backup to your remote storage to prevent data loss", "Sync Failed")
            message.exec_()
            
    def auto_save(self):
        if self.chk_auto_save.isChecked():
            drive_window = DriveWindow()
            drive_window.drive_dict.connect(self.save_drives)
            drive_window.exec_()
        else:   
            auto_save = { "auto_save": False, "google": False, "onedrive": False }
            Model().update("settings", {"auto_save": json.dumps(auto_save)}, "settings")
    
    # Slot to handle the drive_dict signal from the DriveWindow  
    def save_drives(self, drives: object):
        drives["auto_save"] = True
        
        json_string = json.dumps(drives)
        
        Model().update('settings', {'auto_save': json_string}, 'settings')
        
    def manual_remote_save(self, drives):
        if drives["google"]: upload_google(self)
            
    def manual_remote_download(self, drives):
        if drives["google"]:
            self.download_google()
        
        
        
        
            
# This is for the calendar integration
def google_thread():
    print("inside the google thread")
    Google.connect()