import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgets.Widget import Widget
from widgets.TabBar import TabBar
from widgets.TabWidget import TabWidget

main = [
    Widget,
    TabBar,
    TabWidget       
        ]



