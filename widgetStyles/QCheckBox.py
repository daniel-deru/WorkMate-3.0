from msilib.schema import CheckBox
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default
from database.model import Model
from utils.globals import ASSET_PATH
import assets.resources
SIZE = 30
RATIO = 3
width = SIZE * RATIO
height = SIZE * 1

# Get the dark mode setttings
NightModeOn = Model().read("settings")[0][1]

toggle = "toggle-off.svg"
# toggle = "light-toggle-off.svg" if NightModeOn else "dark-toggle-off.svg"

CheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle-on.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle-off.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

"""

SettingsCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
        text-align: left center;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle-on.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle-off.svg);
        width: {width}px;
        height: {height}px;
        max-width: {width}px;
        max-height: {height}px;
        subcontrol-position: right center;
    }}
"""