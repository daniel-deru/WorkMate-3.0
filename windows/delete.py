import os
import sys
from turtle import clear
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt5.QtWidgets import QDialog, QFileDialog, QListView, QCheckBox
from PyQt5.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QFont

from database.model import Model

from widgetStyles.ComboBox import ComboBox
from widgetStyles.PushButton import PushButton
from widgetStyles.Label import Label, LabelLarge
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.Dialog import Dialog

from utils.helpers import StyleSheet, set_font, clear_window


from designs.python.delete_window import Ui_DeleteWindow

group_id_index = {
    'apps': 4,
    'vault': 4,
    'notes': 3,
    'todos': 5
}


class DeleteWindow(Ui_DeleteWindow, QDialog):
    def __init__(self, function) -> None:
        super(DeleteWindow, self).__init__()
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowIcon(QIcon(":/other/app_icon"))
        self.setupUi(self)
        self.cmb_groups.setView(QListView())
        self.cmb_groups.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.set_style()

        self.function = function
        self.function_items = Model().read(function)
        self.groups = Model().read("groups")
        
        self.set_data()
        
        self.cmb_groups.currentIndexChanged.connect(self.set_items)
        self.chk_select_all.stateChanged.connect(self.select_all)
        
    def set_data(self):
        # Set the groups
        for group in self.groups:
            self.cmb_groups.addItem(group[1], group[0])
            
        # Set function name
        self.lbl_function.setText(self.function)
        
        # Set the items
        self.set_items()
        
    def get_current_group_items(self):
        current_group = self.cmb_groups.currentData()
        
        # Get the items for the current group
        current_items_full = list(filter(lambda item: item[group_id_index[self.function]] == str(current_group), self.function_items))
        
        # Get the name and it from the current items
        current_items_part = list(map(lambda item: [item[0], item[1]], current_items_full))
        return current_items_part
    
    def set_items(self):
        clear_window(self.vbox_items)
        current_items = self.get_current_group_items()
        
        for item in current_items:
            id, name = item
            checkbox = QCheckBox(name)
            self.vbox_items.addWidget(checkbox)
    
    # @pyqtSlot(int)
    def select_all(self, checked):
        num_checkboxes = self.vbox_items.count()
        
        for i in range(num_checkboxes):
            checkbox = self.vbox_items.itemAt(i).widget()
            checkbox.setChecked(checked)
                   
    def set_style(self):
        style_list = [
            Label,
            Dialog,
            PushButton,
            CheckBox,
            ComboBox,
            LabelLarge("#lbl_function")
        ]
        
        stylesheet = StyleSheet(style_list).create()
        self.setStyleSheet(stylesheet)
        
        widget_list = [
            self.lbl_function,
            self.lbl_select_group,
            self.btn_delete,
            self.btn_discard,
            self.cmb_groups,
            self.cmb_groups.view(),
            self.chk_select_all
        ]
        set_font(widget_list)
    
        