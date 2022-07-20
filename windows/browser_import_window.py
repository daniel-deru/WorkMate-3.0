from operator import contains
import sys
import os
import json
import pandas as pd

from PyQt5.QtWidgets import (
    QDialog, 
    QTableWidgetItem, 
    QHeaderView, 
    QCheckBox, 
    QStyledItemDelegate, 
    QStyleOptionViewItem, 
    QHBoxLayout, 
    QWidget)
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.browser_import_window import Ui_BrowserPasswordImportWindow

from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog
from widgetStyles.PushButton import PushButton
from widgetStyles.TableWidget import TableWidget
from widgetStyles.ScrollBar import ScrollBar

from utils.helpers import StyleSheet, set_font

from database.model import Model


class BrowserImportWindow(Ui_BrowserPasswordImportWindow, QDialog):
    import_finished = pyqtSignal(list)
    
    def __init__(self, file) -> None:
        super(BrowserImportWindow, self).__init__()
        self.file = file
        self.setupUi(self)
        self.get_file_data()
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        
        # Get the current apps to avoid collisions
        self.current_apps = self.get_current_apps()
        
        self.chk_select_all.stateChanged.connect(self.select_all)
        self.btn_import.clicked.connect(self.import_accounts)
    
    def get_checkboxes(self):
        checkbox_list = []
        number_of_items = self.tbl_accounts.rowCount()
        
        for i in range(number_of_items):
            container_widget: QWidget = self.tbl_accounts.cellWidget(i, 0)
            checkbox: QCheckBox = container_widget.layout().itemAt(0).widget()
            checkbox_list.append(checkbox)
        
        return checkbox_list
    
    def import_accounts(self):
        checkboxes = self.get_checkboxes()
        secrets = list(filter(lambda a: a[1] == "app", Model().read("vault")))
        
        index = len(secrets)
        
        self.import_data = []
        
        self.check = {}
        
        for i in range(len(checkboxes)):
            if checkboxes[i].isChecked():
                name = self.tbl_accounts.item(i, 1).text()
                url = self.tbl_accounts.item(i, 2).text()
                username = self.tbl_accounts.item(i, 3).text()
                password = self.tbl_accounts.item(i, 4).text()
                
                # If the app with this name is already in the database or in the data meant to be imported skip this app
                if name in self.current_apps or name in self.check: continue
                # If the loop didn't continue it's a new app, add it to the check dict
                self.check[name] = name
                
                data: object = {
                    'name': name,
                    'sequence': index,
                    'path': url,
                    'username': username,
                    'email': username,
                    'password': password
                }
                self.import_data.append([name, json.dumps(data)])
                index += 1
                
        self.import_finished.emit(self.import_data)
        self.close()
        
    def select_all(self, checked):
        checkboxes = self.get_checkboxes()
        
        for checkbox in checkboxes:
            if checked:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
        
    def get_file_data(self):
        accounts = pd.read_csv(self.file)
        number_of_rows = len(accounts.index)
        
        self.dup_names = set()
        
        if number_of_rows < 25:
            self.setFixedHeight(200 + number_of_rows * 30)
        else:
            self.setFixedHeight(850)
        
        self.tbl_accounts.setColumnCount(5)
        self.tbl_accounts.setRowCount(number_of_rows)
        
        labels = ["Import", "Name", "URL", "Username", "Password"]
        self.tbl_accounts.setHorizontalHeaderLabels(labels)
        # for i in range(len(labels)):
        #     print(self.tbl_accounts.verticalHeaderItem(i))
            # self.tbl_accounts.horizontalHeaderItem(i).setText(labels[i])
        
        header: QHeaderView = self.tbl_accounts.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        delegate = AlignDelegate(self.tbl_accounts)
        self.tbl_accounts.setItemDelegateForColumn(0, delegate)
        

        for index, item in accounts.iterrows():
            import_checkbox = QCheckBox()
            import_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
            
            container = QWidget()
            container_layout = QHBoxLayout()
            
            container_layout.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(import_checkbox)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container.setLayout(container_layout)

            # This is to accomodate FireFox which uses a different csv format
            name = item['name'] if "name" in item else item['httpRealm']
            self.dup_names.add(name)
            
            self.tbl_accounts.setCellWidget(index, 0, container)
            self.tbl_accounts.setItem(index, 1, QTableWidgetItem(str(name)))
            self.tbl_accounts.setItem(index, 2, QTableWidgetItem(str(item['url'])))
            self.tbl_accounts.setItem(index, 3, QTableWidgetItem(str(item['username'])))
            self.tbl_accounts.setItem(index, 4, QTableWidgetItem(str(item['password'])))
            
    def read_styles(self):
        stylesheet = StyleSheet([Dialog, TableWidget, ScrollBar, PushButton]).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.label,
            self.btn_import,
            self.chk_select_all,
            self.tbl_accounts,
            self.tbl_accounts.horizontalHeader(),
            self.tbl_accounts.verticalHeader()
        ]
        set_font(font_list)
    
    def get_current_apps(self):
        vault_items: list[list[int, str, str, str]] = Model().read("vault")
        current_app_list = list(filter(lambda item: item[1] == "app", vault_items))
        
        current_apps: object = {}
        
        for app in current_app_list:
            current_apps[app[2]] = app
            
        return current_apps
        
class AlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter