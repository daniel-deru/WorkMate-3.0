import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button, green, dark_blue, light_blue

PushButton = f"""
    QPushButton {{
    background-color: {dark_blue};
    color: white;
    border: 2px solid {dark_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 200px;
    min-width: 100px
}}

QPushButton:hover {{
    background-color: {green};
    color: {dark_blue};
    border: 2px solid {green};
}}

QPushButton:pressed {{
    background-color: transparent;
    color: black;
    border: 2px solid {green};
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
