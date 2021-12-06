import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

TextEdit = f"""
    QTextEdit{{
        background-color: {colors['background']};
        color: {colors['text']};
        border-radius: 5px;
        font-size: 16px;
        border: 2px solid {colors['border']};
    }}
"""