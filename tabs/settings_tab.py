import sys
import os
import threading

from PyQt5.QtWidgets import QWidget
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

from windows.timer_window import Timer
from windows.forgot_question import PasswordQuestion
from windows.twofa_window import TwofaDialog
from windows.loading import Loading

from workers.google_download_worker import GoogleDownload

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


        # Signals
        
        self.chkbox_nightmode.stateChanged.connect(self.set_night_mode)
        self.chkbox_2fa.stateChanged.connect(self.twofa)
        self.chkbox_calendar.stateChanged.connect(self.calendar_toggle)
        
        self.btn_login.clicked.connect(self.login_clicked)
        self.btn_forgot_password.clicked.connect(self.forgot_password_clicked)
        self.btn_google_drive_sync.clicked.connect(self.sync_google)
        self.btn_save_google_drive.clicked.connect(self.save_to_google_drive)
        
        

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
        # print(self.styleSheet())
    
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
        
    def sync_google(self):
        
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

        
    def save_to_google_drive(self):
        Google.upload_backup()
        message: Message = Message("The backup is complete", "Backup Successful")
        message.exec_()
        
    def update_db(self, name: str):
        if Model().is_valid(name):
            os.replace(name, f"{DB_PATH}test.db")
            # message: Message = Message("Your data has been synced from google", "Sync Successful")
            # message.exec_()
        else:
            message: Message = Message("Your data on the cloud was corrupted. The data did not sync to your local database. Please save a new working backup to your remote storage to prevent data loss", "Sync Failed")
            message.exec_()
        self.loading.close()
        
            
# @concurrent.process(timeout=30)
def google_thread():
    print("inside the google thread")
    Google.connect()
    
def google_download():
    print("inside download thread")
    Google.download_backup()
    
        


        
