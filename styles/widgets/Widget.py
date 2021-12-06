import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

Widget = f"""
    QWidget {{
        font-size: 16px;
        font-size: 16px;
        padding: 5px 8px;
        background-color: {colors['background']};
    }}
"""

MainWidget = f"""
    QWidget {{
        font-size: 16px;
        font-size: 16px;
        padding: 5px 8px;
        background-color: {colors['text']};
    }}
"""