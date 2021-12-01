import sys
import os
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgets.Label import Label
from widgets.Dialog import Dialog
from widgets.PushButton import PushButton

_widget_list = [
    PushButton,
    Dialog,
    Label
    ]

message_window_styles = reduce(lambda a, b: a + b, _widget_list)