import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, green, light_blue, dark_blue, orange


LineEdit = f"""
    QLineEdit {{
        background-color: {mode};
        color: {default};
        padding: 5px 8px;
        font-size: 16px;
        border-radius: 5px;
        border: 2px solid {dark_blue};
    }}
"""