import sys
import os
import csv
import re
from pebble import concurrent
import threading
import time

from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton, ForgotPasswordButton
from widgetStyles.QCheckBox import SettingsCheckBox
from widgetStyles.ComboBox import ComboBox
from widgetStyles.ScrollBar import ScrollBar

from utils.updateSVG import change_color
from utils.message import Message
from utils.helpers import StyleSheet
from database.model import Model

from windows.timer_window import Timer
from windows.login_window import Login
from windows.forgot_question import PasswordQuestion

from integrations.calendar.c import Google_calendar


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


        self.chkbox_nightmode.setChecked(settings[1])
        self.chkbox_vault.setChecked(settings[4])
        self.chkbox_calendar.setChecked(settings[6])


        self.btn_login.clicked.connect(self.login_clicked)
        self.chkbox_nightmode.stateChanged.connect(self.set_night_mode)
        self.fcmbx_font.currentFontChanged.connect(self.get_font)
        self.btn_reset.clicked.connect(self.reset)
        self.btn_export_apps.clicked.connect(lambda: self.export_data("apps"))
        self.btn_export_notes.clicked.connect(lambda: self.export_data("notes"))
        self.btn_import_apps.clicked.connect(lambda: self.import_data("apps"))
        self.btn_import_notes.clicked.connect(lambda: self.import_data("notes"))
        self.chkbox_vault.stateChanged.connect(self.vault)
        self.btn_vault_timer.clicked.connect(self.vault_timer)
        self.chkbox_calendar.stateChanged.connect(self.calendar_toggle)
        self.btn_forgot_password.clicked.connect(self.forgot_password_clicked)

        # connect the custom signals to the slots
        self.settings_signal.connect(self.read_styles)
        self.login_signal.connect(self.login)

    
    def create_tab(self):
        return self

    # color is at index 3 and nightmode is at index 1
    def set_night_mode(self):
        toggle = self.chkbox_nightmode

        if toggle.isChecked():
            Model().update("settings", {'nightmode': 1}, 'settings')
            self.settings_signal.emit("settings changed")
            self.updateWindow()
        elif not toggle.isChecked():
            Model().update("settings", {'nightmode': 0}, 'settings')
            self.settings_signal.emit("settings changed")
            self.updateWindow()


    def get_font(self):
        font = self.fcmbx_font.currentFont().family()
        Model().update("settings", {'font': font}, 'settings')
        self.settings_signal.emit("settings changed")
    
    def set_font(self):
        font = Model().read('settings')[0][2]
        widget_list = [
            self.lbl_night_mode,
            self.lbl_font,
            self.btn_export_apps,
            self.btn_export_notes,
            self.btn_import_apps,
            self.btn_import_notes,
            self.btn_reset,
            self.btn_vault_timer,
            self.lbl_calendar,
            self.lbl_vault,
            self.lbl_vault_timer,
            self.lbl_reset,
            self.lbl_login,
            self.btn_login
        ]
        for i in range(len(widget_list)):
            widget_list[i].setFont(QFont(font))
        

    def reset(self):
        Model().reset()
        self.settings_signal.emit("settings changed")
        self.chkbox_nightmode.setChecked(False)
    
    def updateWindow(self):
        self.read_styles()
        self.settings_signal.emit("settings")

    def read_styles(self):
        styles = [Label, PushButton, SettingsCheckBox, ComboBox, ScrollBar, ForgotPasswordButton]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        self.set_font()
        


    def export_data(self, table):
        data = Model().read(table)
        if table == "apps":
            def get_website(app):
                website = re.search("^[http(s)?://|www\.]", app[2])
                if website is not None:
                    return app
            data = list(filter(get_website, data))
                
        if len(data) > 0:
            headings = ["name", "path"] if table == "apps" else ["name", "body"]
            with open(f"{DESKTOP}/{table}.csv", 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headings)
                for i in range(len(data)):
                    row = [data[i][1], data[i][2]]
                    writer.writerow(row)

    def import_data(self, table):
        file = QFileDialog.getOpenFileName(self, f"Choose the {table}.csv file", DESKTOP, f"csv files ({table}.csv)")[0]
        field = "body" if table == "notes" else "path"
        fields = []
        with open(file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            if header[1] != field:
                Message("The File does not match the data you want to import. Please ensure you don't change the name of the csv file or import the wrong file.", "File doesn't match data").exec_()
                return
            else:
                for row in reader:
                    fields.append(row)
                if table == "notes":
                    for item in fields:
                        data = {
                            header[0]: item[0],
                            header[1]: item[1]
                        }
                        Model().save(table, data)
                        self.settings_signal.emit("settings")
                elif table == "apps":
                    apps = Model().read("apps")
                    for i in range(len(fields)):
                        data = {
                            header[0]: fields[i][0],
                            header[1]: fields[i][1],
                            'sequence': len(apps) + (i + 1)
                        }
                        Model().save(table, data)
                        self.settings_signal.emit("settings")
    
    def vault(self):
        toggle = self.chkbox_vault
        if self.logged_in:
            if toggle.isChecked():
                Model().update('settings', {"vault_on": 1}, "settings")
                self.login_signal.emit("login requested")
            elif not toggle.isChecked():
                Model().update("settings", {"vault_on": 0}, "settings")

        elif not self.logged_in:
            if not toggle.isChecked():
                Message("The user must be logged in to change this setting", "Please login to change this setting" ).exec_()
                toggle.setChecked(True)
                toggle.setCheckState(Qt.Checked)

        self.updateWindow()
            

    def vault_timer(self):
        vault_on = Model().read("settings")[0][4]
        if not vault_on:
            Message("The vault is not active, please turn on the vault in order to set the timer.", "The vault is off.").exec_()
        elif vault_on and self.logged_in:
                # this is the timer window to set the duration that the user should be logged in
                Timer().exec_()
        elif vault_on and not self.logged_in:
            Message("Please log in before you can change this setting", "user not logged in").exec_()
    
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
            Model().update("settings", {"calendar": 1}, "settings")
        elif not toggle.isChecked():
            Model().update("settings", {"calendar": 0}, "settings")

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
        


            
# @concurrent.process(timeout=30)
def google_thread():
    print("inside the google thread")
    Google_calendar.connect()
    
        


        
