import sys
import os

from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from designs.python.apps_widget import Ui_apps_tab
from PyQt5.QtWidgets import QWidget

from windows.apps_window import Apps_window

from styles.tabs.apps import apps


class Apps_tab(QWidget, Ui_apps_tab):
    def __init__(self):
        super(Apps_tab, self).__init__()
        self.setupUi(self)
        self.read_styles()

        self.btn_add_app.clicked.connect(self.add_app)
    
    def create_tab(self):
        return self

    def read_styles(self):
        styles = reduce(lambda a, b: a + b, apps)
        self.setStyleSheet(styles)

    def add_app(self):
        app_window = Apps_window()
        app_window.exec_()





# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     apps_tab = QWidget()
#     ui = Ui_apps_tab()
#     ui.setupUi(apps_tab)
#     apps_tab.show()
#     sys.exit(app.exec_())

