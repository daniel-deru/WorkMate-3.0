import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors


LineEdit = f"""
    QLineEdit {{
        background-color: {colors['background']};
        color: {colors['text']};
        padding: 5px 8px;
        font-size: 16px;
        border-radius: 5px;
        border: 2px solid {colors['border']};
    }}
"""