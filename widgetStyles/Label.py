import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

Label = f"""
    QLabel{{
        color: {default};
        font-size: 16px;
        border: none;
    }}
"""

LabelMono = f"""
QLabel{{
        color: {default};
        font-size: 16px;
        border: none;
    }}
"""

