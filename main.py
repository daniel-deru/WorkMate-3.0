import sys
import time
import re

from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import QCoreApplication, QTimer


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




class Main(QWidget, Ui_main_container):
    def __init__(self):
        super(Main, self).__init__()
        
        Model().start()

        self.timer = QTimer(self)
        self.logged_in = False
        self.count = 0

        self.setWindowIcon(QIcon("./assets/WorkMate.ico"))
        self.setupUi(self)
        self.read_style()
        self.add_tabs()
        self.setTabIcons()
        self.tab_widget.currentChanged.connect(self.changed)

        user = Model().read("user")
        if len(user) != 1:
            register = Register()
            register.register_close_signal.connect(self.register_event)
            register.exec_()

    def register_event(self, event):
        if event == "window closed":
            print(event)
            sys.exit()
    
            
        
       
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
        self.setMinimumSize(1000, 600)
        # self.tab_widget.setTabPosition(QTabWidget.West)
        self.apps_tab = Apps_tab().create_tab()
        self.apps_tab.table_signal.connect(self.updateTable)
        self.apps_tab.login_signal.emit("logged out")
        self.apps_tab.login_signal.connect(self.check_login)
        self.tab_widget.addTab(self.apps_tab, "Apps")

        self.vault_tab = Vault_tab().create_tab()
        self.tab_widget.addTab(self.vault_tab, "Vault")

        self.notes_tab = Notes_tab().create_tab()
        self.tab_widget.addTab(self.notes_tab, "Notes")

        self.todo_tab = Todo_tab().create_tab()
        self.tab_widget.addTab(self.todo_tab, "To-dos")

        self.settings_tab = SettingsTab().create_tab()
        self.settings_tab.settings_signal.connect(self.updateWindow)
        self.tab_widget.addTab(self.settings_tab, "Settings")

        self.main_layout.addWidget(self.tab_widget)

    def setTabIcons(self):
        stylesheet = self.tab_widget.styleSheet()
        colorWidget = re.search(r"QTabBar::tab {(.|\n|\r)*}", stylesheet).group()
        activeColorWidget = re.search(r"QTabBar::tab:selected {(.|\n|\r)*}", stylesheet).group()

        color = re.search(r"(?<=(?<!background-)color: )#.{6}(?=;)", colorWidget).group()
        activeColor = re.search(r"(?<=(?<!background-)color: )#.{6}(?=;)", activeColorWidget).group()
        icons = [
                "_apps.svg",
                "_vault.svg",
                "_notes.svg",
                "_task.svg",
                "_settings.svg"
        ]
        for i in range(len(icons)):
            icon_color = "black" if color == "#000000" else "white"
            active_icon_color = "black" if activeColor == "#000000" else "white" if activeColor == "#ffffff" else "color"
            self.tab_widget.setTabIcon(i, QIcon(f"./assets/{icon_color}{icons[i]}"))

        active_tab_index = self.tab_widget.currentIndex()
        self.tab_widget.setTabIcon(active_tab_index, QIcon(f"./assets/{active_icon_color}{icons[active_tab_index]}"))
    
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

    
    def login(self, signal):
        if signal == "success":
            self.update_status(True)

            

    def start_timer(self):
        self.count -= 1
        if self.count == 0:
            self.update_status(False)
    
    def update_status(self, logged_in):
        if logged_in:
            self.logged_in = True
            self.apps_tab.login_signal.emit("logged in")
            self.count = Model().read("settings")[0][5] * 60
            self.timer.timeout.connect(self.start_timer)
            self.timer.start(1000)
        elif not logged_in:
            self.count = 0
            self.logged_in = False
            self.apps_tab.login_signal.emit("logged out")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash_image = QPixmap("assets/splash.svg").scaled(500, 500)
    splash = QSplashScreen(splash_image)
    splash.setMaximumWidth(500)
    splash.show()
    time.sleep(1)
    splash.close()
    main = Main()
    main.show()
    sys.exit(app.exec_())