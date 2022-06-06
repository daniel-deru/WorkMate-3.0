import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, light_blue

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