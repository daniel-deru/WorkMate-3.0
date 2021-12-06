import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors
from styles.styles import button_filled

PushButton = f"""
    QPushButton {{
    background-color: {button_filled['background']};
    color: {button_filled['color']};
    border: 2px solid {colors['border']};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
}}

QPushButton:pressed {{
    background-color: {button_filled['background-clicked']};
    color: {button_filled['color-clicked']};
    border: 2px solid {colors['border']};
}}
"""

IconButton = """
    QPushButton {
    background-color: transparent;
    font-size: 16px;
    border: none;
    width: 20px;
}
"""
