import sys
from functools import reduce
import re

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget


from designs.python.main_widget import Ui_main_container
from tabs.apps_tab import Apps_tab

from database.model import Model

from tabs.apps_tab import Apps_tab
from tabs.notes_tab import Notes_tab
from tabs.todos_tab import Todo_tab
from tabs.settings_tab import SettingsTab

from widgetStyles.TabBar import TabBar
from widgetStyles.Widget import Widget
from utils.helpers import StyleSheet




class Main(QWidget, Ui_main_container):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.read_style()
        self.add_tabs()
        
       
    def read_style(self):
        styles = [Widget, TabBar]
        stylesheet = StyleSheet(styles).create()
        self.tab_widget.setStyleSheet(stylesheet)
      
       

    def updateWindow(self):     
        self.read_style()
        self.apps_tab.app_signal.emit("update")
        self.notes_tab.note_signal.emit("update")
        self.todo_tab.todo_signal.emit("update")

    def add_tabs(self):
        self.setMinimumSize(1000, 600)
        
        self.apps_tab = Apps_tab().create_tab()
        self.tab_widget.addTab(self.apps_tab, "Apps")

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
    main = Main()
    main.show()
    sys.exit(app.exec_())

