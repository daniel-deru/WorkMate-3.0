from datetime import date, datetime
import sys
import time
import json
from turtle import update
import assets.resources

from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor, QCloseEvent, QFontDatabase, QShowEvent
from PyQt5.QtCore import QTimer, Qt, pyqtSlot

from designs.python.main_widget import Ui_main_container
from tabs.apps_tab import Apps_tab

from database.model import Model

from tabs.apps_tab import Apps_tab
from tabs.notes_tab import Notes_tab
from tabs.todos_tab import Todo_tab
from tabs.settings_tab import SettingsTab
from tabs.vault_tab import Vault_tab

from widgetStyles.TabBar import TabBar
from widgetStyles.TabWidget import TabWidget
from widgetStyles.Widget import Widget

from utils.helpers import StyleSheet

from windows.register_window import Register
from windows.login_window import Login
from windows.setup_window import InitialSetup
from windows.update_password import UpdatePassword

from threads.google_thread import upload_google
from threads.onedrive_thread import upload_onedrive
from threads.update_password_thread import update_password

class Main(Ui_main_container, QWidget):
    def __init__(self):
        super(Main, self).__init__()
        
        self.expired_passwords: list = []
        
        QFontDatabase.addApplicationFont(":/fonts/RobotoCondensed")
        
        self.timer = QTimer(self) 
        self.logged_in = False
        self.count = 0
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setWindowTitle("TrustLock")
        self.read_style()
        self.add_tabs()
        self.setTabIcons()
        self.update_status(False)

        self.tab_widget.currentChanged.connect(self.changed)    
        
        self.user = Model().read("user")

        if len(self.user) != 1:
            self.register = Register()
            self.register.register_close_signal.connect(self.register_event)
            self.register.exec_()
        else:
            self.get_user_password_expiration()
            self.get_vault_password_expiration()
            
            # Check if there are any expired passwords
            if len(self.expired_passwords) > 0:
                update_password(self)
        
        
    def get_vault_password_expiration(self):
        # Get all the vault entries
        all_vault_entries = Model().read("vault")
        
        # Get only the app and crypto entries
        app_crypto_entries = list(filter(lambda entry: entry[1] != 'general', all_vault_entries))
        
        for entry in app_crypto_entries:
            vault_data = json.loads(entry[3])
            exp_date_string = vault_data['password_exp']
            
            # Get the datetime object from the date string
            exp_datetime = datetime.strptime(exp_date_string, "%Y-%m-%d")
            
            # Get the date object from the datetime object
            exp_date = date(exp_datetime.year, exp_datetime.month, exp_datetime.day)
            
            # Get the current date
            current_date = date.today()
            
            # Put the expired passwords in the expired passwords list
            if exp_date < current_date:
                self.expired_passwords.append(["vault", entry])
           
    
    def get_user_password_expiration(self):
        password_exp_string: str = self.user[0][6]
        
        # Get the datetime object from the string
        exp_date = datetime.strptime(password_exp_string, "%Y-%m-%d")
        
        # Convert to date objext
        password_exp_date = date(exp_date.year, exp_date.month, exp_date.day)
        
        # Get the current date
        current_date = date.today()
        
        if password_exp_date < current_date:
            self.expired_passwords.append(["user", self.user[0]])
    
    # Get the response from asking if the user wants to update passwords 
    @pyqtSlot(bool)  
    def update_password_response(self, response):
        if response == True:
            update_password_window = UpdatePassword(self.expired_passwords)
            update_password_window.exec_()

    def register_event(self, event):
        if event == "window closed":
            sys.exit()
        elif event == "user created":
            self.register.close()
            InitialSetup().exec_()
     
       
    def read_style(self):
        styles = [TabWidget, Widget, TabBar]
        stylesheet = StyleSheet(styles).create()
        self.tab_widget.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]

        self.tab_widget.setFont(QFont(font))
        self.setTabIcons()
      
       

    def updateWindow(self):     
        self.apps_tab.app_signal.emit("update")
        self.notes_tab.note_signal.emit("update")
        self.todo_tab.todo_signal.emit("update")
        self.vault_tab.vault_signal.emit("update")
        self.read_style()
    
    # This is to update the vault window after a new app has been added
    def updateVault(self):
        pass
    
    def updateTable(self):
        self.vault_tab.vault_signal.emit("update")

    def add_tabs(self):
        app = QApplication.primaryScreen()
        screen = app.size()
        self.setMinimumSize(int(screen.width() * 0.7), int(screen.height() * 0.7))
        # self.tab_widget.setTabPosition(QTabWidget.West)
        self.apps_tab = Apps_tab().create_tab()
        self.apps_tab.table_signal.connect(self.updateTable)
        self.apps_tab.login_signal.connect(self.check_login)
        self.tab_widget.addTab(self.apps_tab, "Apps")

        self.vault_tab = Vault_tab().create_tab()
        self.vault_tab.login_signal.connect(self.check_login)
        self.tab_widget.addTab(self.vault_tab, "Vault")

        self.notes_tab = Notes_tab().create_tab()
        self.tab_widget.addTab(self.notes_tab, "Notes")

        self.todo_tab = Todo_tab().create_tab()
        self.tab_widget.addTab(self.todo_tab, "To-dos")

        self.settings_tab = SettingsTab().create_tab()
        self.settings_tab.settings_signal.connect(self.updateWindow)
        self.settings_tab.login_signal.connect(self.check_login)
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        self.tab_widget.tabBar().setCursor(QCursor(Qt.PointingHandCursor))

        self.main_layout.addWidget(self.tab_widget)

    def setTabIcons(self):

        # Get the night mode setting from the database
        nightModeOn = int(Model().read("settings")[0][1])
        icons = [
                "_apps.svg",
                "_vault.svg",
                "_notes.svg",
                "_task.svg",
                "_settings.svg"
        ]
        for i in range(len(icons)):
            # Set the icon color for the tabbar
            icon_color = "black"
            active_icon_color = "white" if nightModeOn else "black"
            self.tab_widget.setTabIcon(i, QIcon(f":/tabicons/{icon_color}{icons[i]}"))

        active_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabIcon(active_tab_index, QIcon(f":/tabicons/{active_icon_color}{icons[active_tab_index]}"))
    
    def changed(self):
        self.setTabIcons()

    def check_login(self, signal):
        # The user wants to log in

        if signal == "login requested" and self.logged_in == False:
            login_window = Login()
            login_window.login_status.connect(self.login)
            login_window.exec_()
        # The user wants to log out
        elif signal == "logout requested" and self.logged_in == True:
            self.update_status(False)

    # slot for the login window signal to verify if the user successfully logged in
    def login(self, signal):
        if signal == "success":
            self.update_status(True)

            
    # This function gets called at a set interval by timer.timeout
    def start_timer(self):
        self.count -= 1
        if self.count == 0:
            self.update_status(False)
            self.timer.stop()
    
    def update_status(self, logged_in):
        # Check if the user wants authentication to be on
        # vault_on = Model().read("settings")[0][4]
        # vault_on = Model().read("settings")[0][4]
        # If auth is on and the user is logged in
        if logged_in:
            self.logged_in = True
            self.send_signals("logged in")
            self.count = int(Model().read("settings")[0][5]) * 60
            self.timer.timeout.connect(self.start_timer)
            self.timer.start(1000)
        # If auth is on and the user is not logged in
        elif not logged_in:
            self.count = 0
            self.logged_in = False
            self.send_signals("logged out")
        # The auth is off the user is always logged in
        # elif not vault_on:
        #     self.send_signals("logged in")

    def send_signals(self, signal):
        self.apps_tab.login_signal.emit(signal)
        self.settings_tab.login_signal.emit(signal)
        self.vault_tab.login_signal.emit(signal)

    def windowSize(self):
        app = QApplication.instance()

        screen = app.primaryScreen()

        available_size = screen.availableGeometry()
        width = available_size.width()
        height = available_size.height()

        self.setFixedSize(int(width/2), int(height/1.5))
        self.setMaximumSize(int(width/2), int(height/1.5))

    def moveEvent(self, event):
        old_screen = QApplication.screenAt(event.oldPos())
        new_screen = QApplication.screenAt(event.pos())

        if not old_screen == new_screen:
            # self.windowSize() 
            pass
        
    def closeEvent(self, event: QCloseEvent) -> None:
        
        auto_save_json = Model().read("settings")[0][8]
        auto_save_dict = json.loads(auto_save_json)
        
        if not auto_save_dict['auto_save']: return
        
        if auto_save_dict['google']:
            upload_google(self, False)
        if auto_save_dict['onedrive']: 
            upload_onedrive(self, False)  
        return super().closeEvent(event)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_image = QPixmap(":/other/splash.png")
    splash = QSplashScreen(splash_image)
    splash.show()
    time.sleep(1)
    splash.close()
    main = Main()
    main.show()
    sys.exit(app.exec_())