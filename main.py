import sys
import time
import os

from PyQt5.QtWidgets import QApplication, QWidget, QSplashScreen
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase

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




class Main(QWidget, Ui_main_container):
    def __init__(self):
        super(Main, self).__init__()
       
        Model().start()
        

        user = Model().read("user")
        if len(user) != 1:
            self.hide()
            register = Register()
            register.exec_()
        
        self.setupUi(self)
        self.read_style()
        self.add_tabs()
        
       
    def read_style(self):
        styles = [TabWidget, Widget, TabBar]
        stylesheet = StyleSheet(styles).create()
        self.tab_widget.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.tab_widget.setFont(QFont(font))
      
       

    def updateWindow(self):     
        self.apps_tab.app_signal.emit("update")
        self.notes_tab.note_signal.emit("update")
        self.todo_tab.todo_signal.emit("update")
        self.read_style()

    def add_tabs(self):
        self.setMinimumSize(1000, 600)
        
        self.apps_tab = Apps_tab().create_tab()
        self.tab_widget.addTab(self.apps_tab, "Apps")

        self.vault_tab = Vault_tab().create_tab()
        self.tab_widget.addTab(self.vault_tab, "Vault")

        self.notes_tab = Notes_tab().create_tab()
        self.tab_widget.addTab(self.notes_tab, "Notes")

        self.todo_tab = Todo_tab().create_tab()
        self.tab_widget.addTab(self.todo_tab, "Todos")

        self.settings_tab = SettingsTab().create_tab()
        self.settings_tab.settings_signal.connect(self.updateWindow)
        self.tab_widget.addTab(self.settings_tab, "Settings")

        self.main_layout.addWidget(self.tab_widget)
        


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