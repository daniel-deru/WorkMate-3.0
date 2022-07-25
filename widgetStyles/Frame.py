import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, light_blue

from widgetStyles.styles import dark_grey, light_grey
from database.model import Model

dark_mode = int(Model().read("settings")[0][1])

frame_background = dark_grey if dark_mode else light_grey

Frame = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        padding: 0px;
        background-color: {mode};
        color: {default};
        border: 2px solid {light_blue};
    }}
"""

TodoFrameDelete = f"""
        QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #00A62E;
        color: #ffffff;
        max-height: 100px;
        height: 100px;
        padding: 0px;
    }}
"""

TodoFrameComplete = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #A60000;
        color: #ffffff;
        max-height: 100px;
        height: 100px;
        padding: 0px;
    }}
"""


def create_frame(id):
    PassGenFrame = f"""
        QFrame{id}{{
            border-radius: 10px;
            background: {frame_background};
        }}
    """
    return PassGenFrame

PassGenFrame = create_frame