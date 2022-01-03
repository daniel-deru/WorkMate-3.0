import os
import sys

from PyQt5.QtWidgets import QWidget, QHeaderView, QTableWidgetItem, QApplication, QLineEdit, QGraphicsBlurEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.vault_tab import Ui_Vault_tab
from utils.helpers import StyleSheet
from windows.login_window import Login


from widgetStyles.TableWidget import TableWidget
from widgetStyles.PushButton import PushButton

from database.model import Model

class Vault_tab(QWidget, Ui_Vault_tab):
    def __init__(self):
        super(Vault_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        self.load_data()

        QFontDatabase.addApplicationFont("./assets/fonts/redacted-script-regular.ttf")
        self.setFont(QFont("Redacted Script"))
       
        self.tbl_vault.horizontalHeader().setStretchLastSection(True)
        self.tbl_vault.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.btn_login.clicked.connect(self.login)

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
        login = Login()
        login.login_status.connect(self.update_status)
        login.exec_()
    
    def update_status(self, signal):
        if signal == "success":
            self.logged_in = True
    
    def visible(self, is_logged_in):
        if not is_logged_in:
            blur = QGraphicsBlurEffect()
            blur.setBlurRadius(15)
            for i in range(len(self.app_items)):
                username = self.tbl_vault.item(i, 2)
                username.setFont(QFont("Redacted Script"))
                
                password = self.tbl_vault.item(i, 3)
                password.setFont(QFont("Redacted Script"))
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Vault_tab()
    main.show()
    sys.exit(app.exec_())






