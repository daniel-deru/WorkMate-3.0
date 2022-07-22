import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default
from database.model import Model

import assets.resources

dark_mode_on = int(Model().read('settings')[0][1])
SIZE = 18
RATIO = 2
width = SIZE * RATIO
height = SIZE * 1

toggle = "toggle-off.svg"

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
#                       
SettingsCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
        text-align: left center;
        width: {width - 10}px;
        height: {height}px;
        max-width: {width - 10}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/toggle-on.svg);
        width: {width - 10}px;
        height: {height}px;
        max-width: {width - 10}px;
        max-height: {height}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/toggle-off.svg);
        width: {width - 10}px;
        height: {height}px;
        max-width: {width - 10}px;
        max-height: {height}px;
        subcontrol-position: right center;
    }}
"""

WhiteEyeCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_white_open.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_white_closed.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}
"""

BlackEyeCheckBox = f"""
    QCheckBox {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_black_open.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_black_closed.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}
"""
eye = "black" if not dark_mode_on else "white"
id = ""

EyeCheckBox = f"""
    QCheckBox{id} {{
        color: {default};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(:/input/eye_{eye}_open.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}

    QCheckBox::indicator{{
        image: url(:/input/eye_{eye}_closed.svg);
        width: {width * (1/3)}px;
        height: {height * (2/3)}px;
        max-width: {width * (1/3)}px;
        max-height: {height * (2/3)}px;
    }}
"""
def custom_id(id):
    EyeCheckBox = f"""
        QCheckBox{id} {{
            color: {default};
            font-size: 16px;
            border-radius: 5px;
        }}

        QCheckBox{id}::indicator:checked {{
            image: url(:/input/eye_{eye}_open.svg);
            width: {width * (1/3)}px;
            height: {height * (2/3)}px;
            max-width: {width * (1/3)}px;
            max-height: {height * (2/3)}px;
        }}

        QCheckBox{id}::indicator{{
            image: url(:/input/eye_{eye}_closed.svg);
            width: {width * (1/3)}px;
            height: {height * (2/3)}px;
            max-width: {width * (1/3)}px;
            max-height: {height * (2/3)}px;
        }}
    """
    return EyeCheckBox

custom_eye = custom_id

