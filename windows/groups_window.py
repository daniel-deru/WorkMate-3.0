import sys
import os
from tokenize import group

from colorama import Style
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QWidget
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot, QSize
from PyQt5.QtGui import QFont, QIcon


from designs.python.groups_window import Ui_GroupsWindow

from database.model import Model

from windows.group_window import GroupWindow

from widgets.group_widget import GroupWidget

from utils.helpers import StyleSheet, set_font

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog

class GroupsWindow(Ui_GroupsWindow, QDialog):
    def __init__(self) -> None:
        super(GroupsWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.set_groups()
        self.get_group_data()
        self.read_styles()
        
        self.btn_add_group.clicked.connect(self.add_group)
        
    def read_styles(self):
        widget_list = [Dialog, PushButton, Label]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_groups,
            self.btn_add_group
        ]
        set_font(font_list)
        
    def add_group(self):
        manage_group_window = GroupWindow()
        manage_group_window.group_add_signal.connect(self.set_groups)
        manage_group_window.exec_()
        
    def set_groups(self):
        groups = Model().read("groups")
        group_data = self.get_group_data()
        for group in groups:
            group_widget = GroupWidget(group, group_data[str(group[0])])
            self.vbox_group_container.addWidget(group_widget)
            
    def get_group_data(self):
        group_dict = {}
        apps = Model().read("apps") # 4 index of group_id
        vault = Model().read("vault") # 4 index of group_id
        notes = Model().read("notes") # 3 index of group_id
        todos = Model().read("todos") # 5 index of group_id
        
        self.create_feature_groups(apps, 4, group_dict, "apps")
        self.create_feature_groups(vault, 4, group_dict, "vault")
        self.create_feature_groups(notes, 3, group_dict, "notes")
        self.create_feature_groups(todos, 5, group_dict, "todos")
        
        return group_dict
        
        
    def create_feature_groups(self, table_data, group_id_index, group_dict, feature):

        for entry in table_data:
            group_id = entry[group_id_index]
            if group_id in group_dict:
                if feature in group_dict[group_id]:
                    group_dict[group_id][feature].append(entry[1])
                else:
                    group_dict[group_id][feature] = [entry[1]]
            else:
                group_dict[group_id] = {feature: [entry[1]]}
        
        
        