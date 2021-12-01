import sys
from functools import reduce

from PyQt5.QtWidgets import QApplication, QWidget

from designs.python.main_widget import Ui_main_container
from tabs.apps_tab import Apps_tab


from tabs.apps_tab import Apps_tab
from tabs.notes_tab import Notes_tab
from tabs.todos_tab import Todo_tab

from styles.tabs.main import main


class Main(QWidget, Ui_main_container):
    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.read_style()

        self.apps_tab = Apps_tab().create_tab()
        self.tab_widget.addTab(self.apps_tab, "Apps")

        self.notes_tab = Notes_tab().create_tab()
        self.tab_widget.addTab(self.notes_tab, "Notes")

        self.todo_tab = Todo_tab().create_tab()
        self.tab_widget.addTab(self.todo_tab, "Todos")
    
    def read_style(self):
        style = reduce(lambda a, b: a + b, main)
        self.setStyleSheet(style)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())