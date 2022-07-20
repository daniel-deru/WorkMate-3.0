import sys
import os
import json
from threading import Thread
from tkinter.ttk import Style

from PyQt5.QtWidgets import (
    QDialog, 
    QCheckBox,
    QHBoxLayout, 
    QWidget,
    QFileDialog)
from PyQt5.QtGui import QCursor, QIcon, QCloseEvent
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.setup_window import Ui_InitialSetup

from database.model import Model

from windows.twofa_window import TwofaDialog
from windows.browser_import_window import BrowserImportWindow

from threads.browser_import_thread import browser_import

from utils.globals import DESKTOP
from utils.helpers import StyleSheet

from integrations.calendar.c import Google

from widgets.setup_widget import SetupWidget

from integrations.graph_api import Microsoft

from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label
from widgetStyles.Dialog import Dialog

class InitialSetup(Ui_InitialSetup, QDialog):
    def __init__(self) -> None:
        super(InitialSetup, self).__init__()
        self.setupUi(self)
        
        self.auto_save_google = False
        self.auto_save_onedrive = False
        
        # This list will be passed to the StackedWidget Item to show the message and run the respective function
        self.setup_list = [
            ["Do you want to use two factor authentication?", "https://smartmetatec.com", self.setup_twofa],
            ["Do you want to turn on dark mode?", None, self.setup_night_mode],
            ["Do you want to import passwords from browser?", "https://smartmetatec.com", self.setup_import_browser],
            ["Do you want to sync with Google Calendar?", "https://smartmetatec.com", self.setup_calendar],
            ["Do you want to automatically save database to Google Drive?", "https://smartmetatec.com", self.setup_google_drive],
            ["Do you want to automatically save database to OneDrive?", "https://smartmetatec.com", self.setup_onedrive],
        ]
        self.create_stack()
        self.read_styles()
        
        self.btn_skip.clicked.connect(self.close)
        
    def read_styles(self):
        widget_list = [
            PushButton,
            Label,
            Dialog
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        self.lbl_setup.setStyleSheet("font-size: 20px;font-weight: bold;")
    
    def create_stack(self):        
        for i in range(len(self.setup_list)):
            step_string = f"Step {i+1} of {len(self.setup_list)}"
            widget_instance = SetupWidget([*self.setup_list[i], step_string])
            widget_instance.next_signal.connect(self.next_widget)
            widget = widget_instance.create_widget()
            self.stack_widget.addWidget(widget)
            
    def next_widget(self):
        current_index = self.stack_widget.currentIndex()
        
        if current_index >= len(self.setup_list) - 1:
            self.close()
        self.stack_widget.setCurrentIndex(current_index + 1)
            
              
    def setup_twofa(self):
        Model().update("settings", {'twofa': '1'}, 'settings')
        twofa_window = TwofaDialog()
        twofa_window.exec_()
        
    def setup_night_mode(self):
        Model().update("settings", {'nightmode': "1"}, 'settings')
        
    def setup_import_browser(self):
        file = QFileDialog.getOpenFileName(self, "Choose a file", DESKTOP, f"CSV File (*.csv)")[0]
        if file:
            browser_window = BrowserImportWindow(file)
            browser_window.import_finished.connect(lambda data: browser_import(self, data))
            browser_window.exec_()
            
    def setup_calendar(self):
        th = Thread(target=google_thread, daemon=True)
        th.start()
        Model().update("settings", {"calendar": "1"}, "settings")
        
    def setup_google_drive(self):
        self.auto_save_google = True
        # thread = Thread(target=google_thread, daemon=True)
        # thread.start()
        Google.connect()

    def setup_onedrive(self):
        self.auto_save_onedrive = True
        # thread = Thread(target=microsoft_thread, daemon=True)
        # thread.start()
        Microsoft()
        
    def closeEvent(self, event: QCloseEvent) -> None:
        auto_save = {
            "auto_save": False,
            "google": False,
            "onedrive": False
        }
        
        if self.auto_save_google: auto_save['google'] = True      
        if self.auto_save_onedrive: auto_save['onedrive'] = True
        
        if auto_save['google'] or auto_save['onedrive']:
            auto_save['auto_save'] = True
            Model().update('settings', {'auto_save': json.dumps(auto_save)}, 'settings')

        return super().closeEvent(event)
    
    def updateWindow(self):
        pass
        
def google_thread():
    print("inside the google thread")
    Google.connect()
    
def microsoft_thread():
    Microsoft()
    
            
    
        
    