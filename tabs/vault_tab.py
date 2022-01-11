import os
import sys
import pyperclip
import time
import threading

from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt5.QtGui import QFont, QFontDatabase


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab
from utils.helpers import StyleSheet
from utils.message import Message
from windows.login_window import Login


from widgetStyles.TableWidget import TableWidget
from widgetStyles.PushButton import PushButton

from database.model import Model

class Vault_tab(QWidget, Ui_Vault_tab):
    vault_signal = pyqtSignal(str)
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        # self.load_data()
        self.timer = QTimer(self)
        QFontDatabase.addApplicationFont("./assets/fonts/redacted-script-regular.ttf")
       
        self.tbl_vault.horizontalHeader().setStretchLastSection(True)
        self.tbl_vault.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.btn_login.clicked.connect(self.login)
        self.tbl_vault.itemClicked.connect(self.item)
        self.btn_username.clicked.connect(self.show_user)
        self.btn_password.clicked.connect(self.show_password)
        self.vault_signal.connect(self.update)

        self.logged_in = False
        self.user_visibility = False
        self.password_visibility = False
        self.count = 0
        # self.visible()

    def load_data(self):
        def filterApps(app):
            if app[4] and app[5]:
                return True
        
        def mapApps(app):
            return [
                app[1],
                app[2],
                app[4],
                app[5]
            ]
        filter_app_items = list(filter(filterApps, Model().read("apps")))
        self.app_items = list(map(mapApps, filter_app_items))
        self.tbl_vault.setRowCount(len(self.app_items))

        for i in range(len(self.app_items)):
            row = i
            for j in range(len(self.app_items[row])):
                col = j
                item = QTableWidgetItem(self.app_items[row][col])
                item.setFlags(Qt.ItemIsEnabled)
                self.tbl_vault.setItem(row, col, item)

     
    
    def create_tab(self):
        return self

    def read_styles(self):
        styles = [
            TableWidget,
            PushButton
        ]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)

    def login(self):
        if not self.logged_in:
            login = Login()
            login.login_status.connect(self.update_status)
            login.exec_()
            
            if self.logged_in:
                self.count = Model().read("settings")[0][5] * 60
                self.timer.timeout.connect(self.start_timer)
                self.timer.start(1000)
                
                
        else:
            self.logged_in = False
            self.visible()
            self.timer.stop()
            self.btn_login.setText("login")
    
    def update_status(self, signal):
        if signal == "success":
            self.logged_in = True
            self.visible()
            self.btn_login.setText("Logout")
    
    def visible(self):
        font = Model().read("settings")[0][2]
        vault_on = Model().read("settings")[0][4]
        for i in range(len(self.app_items)):
            username = self.tbl_vault.item(i, 2)
            password = self.tbl_vault.item(i, 3)
            
            if vault_on:
                username.setFont(QFont("Redacted Script", 20))
                password.setFont(QFont("Redacted Script", 20))
                if self.logged_in:
                    if self.user_visibility:
                        username.setFont(QFont(font))
                    if self.password_visibility:
                        password.setFont(QFont(font))
                elif not self.logged_in:
                    username.setFont(QFont("Redacted Script", 20))
                    password.setFont(QFont("Redacted Script", 20))

            elif not vault_on:
                username.setFont(QFont(font))
                password.setFont(QFont(font))

    def update(self):
        for i in range(self.tbl_vault.rowCount()):
            self.tbl_vault.removeRow(i)
        self.load_data()
        self.visible()
        self.read_styles()
        self.tbl_vault.setMaximumSize(self.getQTableWidgetSize())
        self.tbl_vault.setMinimumSize(self.getQTableWidgetSize())
    
    def getQTableWidgetSize(self):
        w = self.tbl_vault.verticalHeader().width() + 4  # +4 seems to be needed
        for i in range(self.tbl_vault.columnCount()):
            w += self.tbl_vault.columnWidth(i)  # seems to include gridline (on my machine)
        h = self.tbl_vault.horizontalHeader().height() + 4
        for i in range(self.tbl_vault.rowCount()):
            h += self.tbl_vault.rowHeight(i)
        return QSize(w, h)

    def item(self, item):
        column = item.column()
        vault_on = Model().read("settings")[0][4]

        if self.logged_in and (column == 2 or column == 3) or not vault_on:
            pyperclip.copy(item.text())
        elif not self.logged_in and (column == 2 or column == 3):
            Message("Please login before you can access this information.", "Restricted Access").exec_()

    def show_user(self):
        if self.logged_in:
            self.user_visibility = not self.user_visibility
            self.visible()
        else:
            Message("Please login before you can view the usernames.", "Restricted Access").exec_()

    def show_password(self):
        if self.logged_in:
            self.password_visibility = not self.password_visibility
            self.visible()
        else:
            Message("Please login before you can view the passwords.", "Restricted Access").exec_()

    def start_timer(self):
        self.count -= 1
        print(self.count)
        if self.count == 0:
            self.login()

        



    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Vault_tab()
    main.show()
    sys.exit(app.exec_())






