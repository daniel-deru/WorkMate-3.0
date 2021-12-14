import sys
import os
import csv
import re

from PyQt5.QtWidgets import QWidget, QColorDialog, QFileDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.settings_tab import Ui_Settings_tab

from widgetStyles.Label import Label
from widgetStyles.PushButton import PushButton
from widgetStyles.QCheckBox import CheckBox
from widgetStyles.ComboBox import ComboBox
from utils.helpers import StyleSheet
from utils.message import Message
from database.model import Model

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))


class SettingsTab(QWidget, Ui_Settings_tab):
    settings_signal = pyqtSignal(str)
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.read_styles()
        settings = Model().read('settings')[0]
        nightmode = settings[1]
        self.chkbx_night_mode.setChecked(nightmode)

        self.chkbx_night_mode.stateChanged.connect(self.set_night_mode)
        self.btn_color.clicked.connect(self.set_color)
        self.fcmbx_font.currentFontChanged.connect(self.set_font)
        self.btn_reset.clicked.connect(self.reset)
        self.settings_signal.connect(self.read_styles)
        self.btn_export_apps.clicked.connect(lambda: self.export_data("apps"))
        self.btn_export_notes.clicked.connect(lambda: self.export_data("notes"))
        self.btn_import_apps.clicked.connect(lambda: self.import_data("apps"))
        self.btn_import_notes.clicked.connect(lambda: self.import_data("notes"))        
    
    def create_tab(self):
        return self

    def set_night_mode(self):
        print("clicked", self.chkbx_night_mode.isChecked())
        color = Model().read('settings')[0][3]
        if color == "#000000":
            Message("Nightmode is not available with the default color. Please choose a different color.", "Night Mode not available").exec_()
            self.chkbx_night_mode.setChecked(False)
        else:
            nightmode = self.chkbx_night_mode.isChecked()
            Model().update("settings", {'nightmode': nightmode}, 'settings')
            self.settings_signal.emit("settings changed")
            self.updateWindow()

    def set_font(self):
        font = self.fcmbx_font.currentFont().family()
        Model().update("settings", {'font': font}, 'settings')
        self.settings_signal.emit("settings changed")
        

    def set_color(self):
        color = QColorDialog().getColor().name()
        Model().update("settings", {'color': color}, 'settings')
        self.settings_signal.emit("settings changed")

    def reset(self):
        Model().reset()
        self.settings_signal.emit("settings changed")
    
    def updateWindow(self):
        self.read_styles()
        self.settings_signal.emit("settings")

    def read_styles(self):
        styles = [Label, PushButton, CheckBox, ComboBox]
        stylesheet = StyleSheet(styles).create()
        self.setStyleSheet(stylesheet)
        font = Model().read('settings')[0][2]
        self.lbl_color.setFont(QFont(font))
        self.lbl_night_mode.setFont(QFont(font))
        self.lbl_font.setFont(QFont(font))
        self.btn_color.setFont(QFont(font))
        self.btn_export_apps.setFont(QFont(font))
        self.btn_export_notes.setFont(QFont(font))
        self.btn_import_apps.setFont(QFont(font))
        self.btn_import_notes.setFont(QFont(font))
        self.btn_reset.setFont(QFont(font))

    def export_data(self, table):
        data = Model().read(table)
        if table == "apps":
            def get_website(app):
                website = re.search("^[http(s)?://|www\.]", app[2])
                if website is not None:
                    return app
            data = list(filter(get_website, data))
            print(data)
                
        if len(data) > 0:
            headings = ["name", "path"] if table == "apps" else ["name", "body"]
            with open(f"{DESKTOP}/{table}.csv", 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headings)
                for i in range(len(data)):
                    row = [data[i][1], data[i][2]]
                    writer.writerow(row)

    def import_data(self, table):
        file = QFileDialog.getOpenFileName(self, f"Choose the {table}.csv file", DESKTOP, f"csv files ({table}.csv)")[0]
        field = "body" if table == "notes" else "path"
        fields = []
        with open(file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            if header[1] != field:
                Message("The File does not match the data you want to import. Please ensure you don't change the name of the csv file or import the wrong file.", "File doesn't match data").exec_()
                return
            else:
                for row in reader:
                    fields.append(row)
                if table == "notes":
                    for item in fields:
                        data = {
                            header[0]: item[0],
                            header[1]: item[1]
                        }
                        Model().save(table, data)
                        self.settings_signal.emit("settings")
                elif table == "apps":
                    apps = Model().read("apps")
                    for i in range(len(fields)):
                        data = {
                            header[0]: fields[i][0],
                            header[1]: fields[i][1],
                            'sequence': len(apps) + (i + 1)
                        }
                        Model().save(table, data)
                        self.settings_signal.emit("settings")
        
