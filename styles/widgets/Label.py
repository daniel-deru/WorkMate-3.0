import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

Label = f"""
    QLabel{{
        color: {colors['text']};
        font-size: 16px;
        border: none;
    }}
"""