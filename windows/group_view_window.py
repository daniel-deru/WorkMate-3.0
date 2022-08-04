import sys
import os
from tkinter import font
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from designs.python.group_view_window import Ui_GroupWindow

from utils.helpers import StyleSheet

from widgetStyles.Label import Label, LabelLarge
from widgetStyles.PushButton import PushButton
from widgetStyles.Dialog import Dialog

from utils.helpers import set_font
class GroupViewWindow(Ui_GroupWindow, QDialog):
    def __init__(self, group, group_data) -> None:
        super(GroupViewWindow, self).__init__()
        self.group = group
        self.group_data = group_data
        self.setupUi(self)
        self.read_styles()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.display_data()
        
    def read_styles(self):
        widget_list = [
            Dialog, 
            PushButton, 
            Label,
            LabelLarge("#lbl_group_name")
        ]
        
        stylesheet = StyleSheet(widget_list).create()
        self.setStyleSheet(stylesheet)
        
        font_list = [
            self.lbl_apps,
            self.lbl_apps_display,
            self.lbl_description,
            self.lbl_group_name,
            self.lbl_notes,
            self.lbl_notes_display,
            self.lbl_todos,
            self.lbl_todos_display,
            self.lbl_vault,
            self.lbl_vault_display,
            self.btn_delete
        ]
        set_font(font_list)
        
    def display_data(self):
        self.lbl_group_name.setText(self.group[1])
        self.lbl_description.setText(self.group[2])
        
        display_widget = {
            'apps': self.lbl_apps_display,
            'vault': self.lbl_vault_display,
            'notes': self.lbl_notes_display,
            'todos': self.lbl_todos_display
        }
        
        for feature in self.group_data:
            count = len(self.group_data[feature])
            display_widget[feature].setText(str(count))
        
    
        
    
