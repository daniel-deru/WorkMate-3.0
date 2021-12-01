import sys
import os
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgets.PushButton import PushButton
from widgets.LineEdit import LineEdit
from widgets.QCheckBox import CheckBox
from widgets.TextEdit import TextEdit
from widgets.Widget import Widget
from widgets.Dialog import Dialog

_widget_list = [
    PushButton,
    LineEdit,
    CheckBox,
    TextEdit,
    Widget,
    Dialog
]

note_window_styles = reduce(lambda a, b: a + b, _widget_list)