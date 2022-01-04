import os
import sys
import pyperclip

from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QApplication
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QFontDatabase


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab
from utils.helpers import StyleSheet
from utils.message import Message
from utils.helpers import clear_window
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
        self.load_data()

        QFontDatabase.addApplicationFont("./assets/fonts/redacted-script-regular.ttf")
       
        self.tbl_vault.horizontalHeader().setStretchLastSection(True)
        self.tbl_vault.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.btn_login.clicked.connect(self.login)
        self.tbl_vault.itemClicked.connect(self.item)
        self.vault_signal.connect(self.update)

        self.logged_in = False
        self.visible(self.logged_in)

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
        else:
            self.logged_in = False
            self.visible(False)
            self.btn_login.setText("login")
    
    def update_status(self, signal):
        if signal == "success":
            self.logged_in = True
            self.visible(self.logged_in)
            self.btn_login.setText("Logout")
    
    def visible(self, is_logged_in):
        font = Model().read("settings")[0][2]
        vault_on = Model().read("settings")[0][4]
        for i in range(len(self.app_items)):
            username = self.tbl_vault.item(i, 2)
            password = self.tbl_vault.item(i, 3)

            if not is_logged_in and vault_on:
                username.setFont(QFont("Redacted Script", 20))
                password.setFont(QFont("Redacted Script", 20))
            elif is_logged_in:
                username.setFont(QFont(font))
                password.setFont(QFont(font))
            elif not vault_on:
                username.setFont(QFont(font))
                password.setFont(QFont(font))
    def update(self):
        for i in range(self.tbl_vault.rowCount()):
            self.tbl_vault.removeRow(i)
        self.load_data()
        self.visible(self.logged_in)
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
        if self.logged_in and column == 2 or self.logged_in and column == 3:
            pyperclip.copy(item.text())
        elif not self.logged_in and column == 2 or not self.logged_in and column == 3:
            Message("Please login before you can access this information.", "Restricted Access").exec_()
    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Vault_tab()
    main.show()
    sys.exit(app.exec_())






