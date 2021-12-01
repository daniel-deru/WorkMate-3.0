import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgets.PushButton import PushButton
from widgets.LineEdit import LineEdit
from widgets.QCheckBox import CheckBox

notes = [
    CheckBox,
    PushButton, 
    ]