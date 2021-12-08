import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

SpinBox = f"""
    QSpinBox {{
        background-color: {colors['background']};
        color: {colors['text']};
        font-size: 16px;
        padding: 5px 8px;
        border-radius: 5px;
        border: 2px solid {colors['border']};
    }}

    QSpinBox::down-button {{
        border: none;
        image: url(assets/down.png);
        width: 10px;
        height: 10px;
        padding: 5px 10px; 
    }}
    QSpinBox::up-button {{
        border: none;
        image: url(assets/up.png);
        width: 10px;
        height: 10px;
        padding: 5px 10px; 
    }}
"""