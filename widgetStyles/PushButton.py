import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button

PushButton = f"""
    QPushButton {{
    background-color: {color};
    color: {button};
    border: 2px solid {color};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
}}

QPushButton:pressed {{
    background-color: {mode};
    color: {color};
    border: 2px solid {color};
}}
"""

VaultButton = f"""
  QPushButton {{
    background-color: {color};
    color: {button};
    border: 2px solid {color};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
}}

QPushButton:pressed {{
    background-color: {mode};
    color: {color};
    border: 2px solid {color};
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

AppRunButton = f"""
QPushButton#run {{
    background-color: {color};
    color: #ffffff;
    border: 2px solid {color};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    width: 40px
}}

QPushButton#run:pressed {{
    background-color: {mode};
    color: {color};
    border: 2px solid {color};
}}

"""
