import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgets.PushButton import PushButton
from widgets.LineEdit import LineEdit
from widgets.Label import Label
from widgets.DateEdit import DateEdit
from widgets.Widget import Widget

todo = [
    Widget,
    LineEdit,
    PushButton,
    Label,
    DateEdit
    ]