from math import fabs
import sys
import os
import threading
import shutil
import json

from PyQt5.QtWidgets import QWidget, QFileDialog, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QSize, pyqtSlot
from PyQt5.QtGui import QFont, QIcon, QPixmap

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import IconButton
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox
from widgetStyles.ScrollBar import ScrollBar
from widgetStyles.ToolButton import ToolButton

from utils.message import Message
from utils.helpers import LoginEvent, StyleSheet, set_font
from utils.globals import DB_PATH, PATH, DB_NAME, DESKTOP
from utils.enums import TwofaStatus

from database.model import Model


from windows.forgot_question import PasswordQuestion
from windows.reset_password import ResetPassword
from windows.drive_window import DriveWindow
from windows.twofa_window import TwofaDialog
from windows.browser_import_window import BrowserImportWindow
from windows.generate_password import GeneratePasswordWindow
from windows.setup_window import InitialSetup
from windows.groups_window import GroupsWindow
from windows.timer_window import Timer
from windows.login_window import Login

from threads.google_thread import upload_google, download_google
from threads.onedrive_thread import upload_onedrive, download_onedrive
from threads.browser_import_thread import browser_import

from integrations.calendar.c import Google

class SettingsTab(Ui_Settings_tab, QWidget):
    settings_signal = pyqtSignal(str)
    # This signal will communicate with the main window to get and set the login status
    login_signal = pyqtSignal(str)
    settings_update_signal = pyqtSignal(str)
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.logged_in = False
        self.set_checkboxes()
        self.set_btn_icons()


        # checkbox signals        
        self.chkbox_nightmode.stateChanged.connect(self.set_night_mode)
        self.chkbox_2fa.stateChanged.connect(self.twofa)
        self.chkbox_calendar.stateChanged.connect(self.calendar_toggle)
        # self.chk_auto_save.stateChanged.connect(self.auto_save)
        
        self.btn_auto_save.clicked.connect(self.auto_save)
        
        self.btn_login.clicked.connect(self.login_clicked)
        self.btn_forgot_password.clicked.connect(self.forgot_password_clicked)
        self.btn_google_drive_sync.clicked.connect(self.restore_from_remote)
        self.btn_save_google_drive.clicked.connect(self.save_to_remote_storage)
        self.btn_save_local.clicked.connect(self.save_local)
        self.btn_restore_local.clicked.connect(self.restore_from_local)
        self.btn_browser_web_import.clicked.connect(self.import_websites)
        self.btn_generate_password.clicked.connect(self.generate_password)
        self.btn_setup.clicked.connect(self.setup_wizard)
        self.btn_groups.clicked.connect(self.manage_groups)
        self.btn_update_password.clicked.connect(self.updatePassword)
        
        self.btn_google.clicked.connect(self.google_sign_in)
        self.btn_timer.clicked.connect(self.timer)

        # connect the custom signals to the slots
        self.settings_signal.connect(lambda: self.updateWindow(False))
        self.settings_update_signal.connect(lambda: self.updateWindow(False))
        self.login_signal.connect(self.login)
        
    @pyqtSlot()
    def timer(self):
        if not self.logged_in:
            self.login_clicked()
        else:
            timer_window = Timer()
            timer_window.exec_()
        
    @pyqtSlot()
    def updatePassword(self):
        # Request login even if user is logged in
        # Pass in a variable to determin which signals to send
        login_window = Login(update_password=True)
        login_window.update_password_status.connect(self.update_password)
        login_window.exec_()

    
    @pyqtSlot(str)
    def update_password(self, status: str):
        if(status == "success"):
            update_password_window = ResetPassword(False)
            update_password_window.exec_()
        
    def set_checkboxes(self):
        settings = Model().read('settings')[0]
        # Set the default value of the settings
        self.chkbox_nightmode.setChecked(int(settings[1]))
        self.chkbox_calendar.setChecked(int(settings[6]))
        
        self.chkbox_2fa.blockSignals(True)
        self.chkbox_2fa.setChecked(int(settings[7]))
        self.chkbox_2fa.blockSignals(False)
        
    def manage_groups(self):
        GroupsWindow().exec_()
        
    def setup_wizard(self):
        setup_wizard = InitialSetup()
        setup_wizard.setup_finished.connect(self.updateWindow)
        setup_wizard.exec_()
        
    def generate_password(self):
        generate_password = GeneratePasswordWindow()
        generate_password.exec_()
        
    
    def import_websites(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, f"CSV File (*.csv)")[0]
        if file:
            browser_window = BrowserImportWindow(file)
            browser_window.import_finished.connect(self.import_browser_data)
            browser_window.exec_()
        else:
            Message("Please choose a valid file", "Invalid File").exec_()
    
    def import_browser_data(self, data):
        browser_import(self, data)
    
    def create_tab(self):
        return self

    # color is at index 3 and nightmode is at index 1
    def set_night_mode(self, checked):
        if checked:
            Model().update("settings", {'nightmode': "1"}, 'settings')
        else:
            Model().update("settings", {'nightmode': "0"}, 'settings')
            
        self.updateWindow()
        
    
    # 2fa slot
    def twofa(self, checked):
        toggle = self.chkbox_2fa
        if not self.logged_in:
            toggle.blockSignals(True)
            self.login_clicked()
            toggle.setChecked(not checked)
            state = Qt.Unchecked if checked else Qt.Checked
            toggle.setCheckState(state)
            toggle.blockSignals(False)
        else:
            if checked:
                twofa_window = TwofaDialog()
                twofa_window.twofa_status.connect(self.twofa_status)
                twofa_window.exec_()
            else:
                Model().update('user', {'twofa_key': None}, 'user')
                Model().update("settings", {'twofa': '0'}, 'settings')
    
    @pyqtSlot(TwofaStatus)       
    def twofa_status(self, status: TwofaStatus):
        if status == TwofaStatus.failure:
            self.chkbox_2fa.setChecked(False)
            self.chkbox_2fa.setCheckState(Qt.Unchecked)

    
    def updateWindow(self, send_signal: bool = True):
        self.read_styles()
        self.set_checkboxes()
        if send_signal: self.settings_signal.emit("settings")


    def read_styles(self):
        styles = [
            Label, 
            SettingsCheckBox, 
            ComboBox, 
            ScrollBar, 
            IconButton,
            ToolButton # this is for the google button
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        
        font_widgets = [
            self.lbl_2fa,
            self.lbl_night_mode,
            self.lbl_calendar,
            self.lbl_auto_save,
            self.lbl_login,
            self.lbl_forgot_password,
            self.lbl_browser_web_import,
            self.lbl_save_remote,
            self.lbl_restore_remote,
            self.lbl_save_local,
            self.lbl_restore_local,
            self.lbl_google_integration,
            self.lbl_generate_password,
            self.lbl_setup,
            self.lbl_groups,
            self.lbl_update_password,
            self.lbl_timer,
        ]
        
        set_font(font_widgets)
            
    def set_btn_icons(self):
        # Set the correct size for the google sign in button
        pixmap: QPixmap = QPixmap(":/button_icons/google")
        icon: QIcon = QIcon(pixmap)
        self.btn_google.setIcon(icon)
        self.btn_google.setIconSize(pixmap.rect().size())
        
        self.btn_generate_password.setIcon(QIcon(":/button_icons/password"))
        self.btn_generate_password.setIconSize(QSize(30, 20))
        
        button_icon_list = [
            [self.btn_browser_web_import, ":/button_icons/import"],
            [self.btn_forgot_password, ":/button_icons/reset"],
            [self.btn_login, ":/button_icons/unlock"],
            [self.btn_google_drive_sync, ":/button_icons/cloud_download"],
            [self.btn_save_google_drive, ":/button_icons/cloud_upload"],
            [self.btn_restore_local, ":/button_icons/drive_download"],
            [self.btn_save_local, ":/button_icons/drive_upload"],
            [self.btn_setup, ":/button_icons/setup"],
            [self.btn_groups, ":/button_icons/group"],
            [self.btn_update_password, ":/button_icons/reset"],
            [self.btn_timer, ":/button_icons/timer"],
            [self.btn_auto_save, ":/button_icons/auto_save"]
        ]
        
        for button, icon in button_icon_list:
            button: QPushButton
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(20, 20))
    
    def login(self, signal):
        if signal == "success":
            self.logged_in = True
    
    def check_login(self, signal):
        if signal == "logged in":
            self.logged_in = True
        elif signal == "logged out":
            self.logged_in = False
        
    def google_sign_in(self):
        token_file = f"{PATH}/integrations/google_token.json"
        if not os.path.exists(token_file):
            threading.Thread(target=google_thread, daemon=True).start()
        else:
            Message("You are already integrated with Google Calendar", "No Action Needed").exec_()

    def calendar_toggle(self):
        token_file = f"{PATH}/integrations/google_token.json"
        if not os.path.exists(token_file) and self.chkbox_calendar.checkState() == Qt.Checked:
            Message("Please Allow Trust Lock to integrate with your google account by clicking on The 'Sign in with Google' button", "Not Allowed").exec_()
            self.chkbox_calendar.setChecked(False)
            self.chkbox_calendar.setCheckState(Qt.Unchecked)
        else:
            checked = "1" if self.chkbox_calendar.isChecked() else "0"
            Model().update("settings", {"calendar": checked}, "settings")

    def login_clicked(self):
        if self.logged_in:
            self.login_signal.emit("logout requested")
        elif not self.logged_in:
            self.login_signal.emit("login requested")


    def login(self, signal):
        if signal == "logged in":
            # self.btn_login.setText("Logout")
            self.btn_login.setIcon(QIcon(":/button_icons/lock"))
            self.logged_in = True
        elif signal == "logged out":
            # self.btn_login.setText("Login")
            self.btn_login.setIcon(QIcon(":/button_icons/unlock"))
            self.logged_in = False

    def forgot_password_clicked(self):
        ask_question = PasswordQuestion()
        ask_question.passphrase_signal.connect(lambda: self.updateWindow())
        ask_question.exec_()


    # Slot for the btn_save_google_drive Signal to save to remote storage manually
    def save_to_remote_storage(self):     
        self.drive_window: DriveWindow = DriveWindow()
        self.drive_window.drive_dict.connect(self.manual_remote_save)
        self.drive_window.exec_()
        
    def save_local(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if path: shutil.copy(f"{DB_PATH}{DB_NAME}", f"{path}/{DB_NAME}")
        
    def restore_from_remote(self):
        self.drive_window: DriveWindow = DriveWindow()
        self.drive_window.drive_dict.connect(self.manual_remote_download)
        self.drive_window.exec_()
        
    def restore_from_local(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, f"DB File ({DB_NAME})")[0]
        
        if not file: 
            return

        valid_db, message = self.compare_dbs(file)

        if(not valid_db):
            return Message(message, "Sync Failed")

        shutil.copy(file, f"{DB_PATH}{DB_NAME}")
        self.updateWindow()
        Message("Local data sync was successful.", "Sync Successful").exec_()
            
    def compare_dbs(self, new_db_path):
        new_db = None
    
        try: 
            new_db = Model(new_db_path)
        except Exception:
            return [False, "Unable to open database"]
        
        new_db_user = new_db.read('user')
        
        if(len(new_db_user) < 1):
            return [False, "Invalid database"]
        
        new_db_passphrase = new_db_user[0][4]
        passphrase = Model().read('user')[0][4]
        
        if(new_db_passphrase != passphrase):
            return [False, "The account you are trying to restore is not the same as the account you currently have."]
        
        return [True, None]
            
    def auto_save(self):
        # if self.chk_auto_save.isChecked():
        drive_window = DriveWindow()
        drive_window.drive_dict.connect(self.save_drives)
        drive_window.exec_()
    
    # check if the new db is valid and replace old db with new db
    def update_db(self, name: str or None):
        if(not name):
            self.loading.close()
            return Message("The database does not exist or there is a network error", "Sync Failed").exec_()
        
        valid_db, message = Model().valid_account(f"{DB_PATH}{name}")
        
        if(not valid_db):
            self.loading.close()
            return Message(message, "Sync Error").exec_()

        shutil.move(f"{DB_PATH}{name}", f"{DB_PATH}{DB_NAME}")
        Message("Sync was successful.", "Sync Successful").exec_()
        
        # Close the loading dialog after thread is finished
        self.loading.close()
    
    # Slot to handle the drive_dict signal from the DriveWindow  
    def save_drives(self, drives: object or None) -> None:
        
        if not drives:
            return
        drives["auto_save"] = True
        
        json_string = json.dumps(drives)
        
        Model().update('settings', {'auto_save': json_string}, 'settings')
        
    def manual_remote_save(self, drives):
        self.drive_window.close()
        
        try:
            if drives["google"]:
                upload_google(self)
                
            if drives['onedrive']:
                upload_onedrive(self)
        except Exception as error:
            print("error")
            with open(f"{PATH}error.txt", "a") as error_file:
                error_file.write(f"\n\n{error}")
            
            
    def manual_remote_download(self, drives):
        self.drive_window.close()
        try:
            if drives["google"]:
                download_google(self)
            elif drives['onedrive']:
                download_onedrive(self)
        except Exception as error:
            with open(f"{PATH}error.txt", "a") as error_file:
                error_file.write(f"\n\n{error}")
        self.updateWindow()
        
          
# This is for the calendar integration
def google_thread():
    print("inside the google thread")
    Google.connect()