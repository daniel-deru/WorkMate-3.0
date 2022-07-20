import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, button, green, dark_blue, light_blue, default, orange

PushButton = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 2px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 200px;
    min-width: 100px;
    min-height: 20px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""

PushButton100Width = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 2px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 100px;
    min-width: 100px;
    min-height: 20px;
}}



QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""

PushButtonLink = """
        QPushButton {
            background: transparent;
            color: black;
            border: none;
            width: 100px;
            }

        QPushButton:hover {
            color: blue;
            text-decoration: underline;
        }
"""

ButtonBackIcon = f"""
    QPushButton#btn_back {{
    background-color: transparent;
    text-align: left;
    max-width: 45px;
    min-width: 45px;
    width: 45px;
    height: 45px;
    border: none;
}}
"""

ButtonFullWidth = f"""
    QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 2px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    min-width: 100px;
    max-width: 250px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""

ForgotPasswordButton = f"""
    QPushButton#btn_forgot_password {{
        max-width: 1000px;
    }}
"""

VaultButton = f"""
QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 2px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 300px;
    min-width: 300px;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""
VaultButtonLeftAlign = f"""
QPushButton {{
    background-color: {light_blue};
    color: white;
    border: 2px solid {light_blue};
    border-radius: 5px;
    font-size: 16px;
    padding: 5px 8px;
    max-width: 300px;
    min-width: 300px;
    text-align: left;
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""

IconButton = f"""
    QPushButton {{
    background-color: {light_blue};
    border: none;
    border-radius: 5px;
    width: 70px;
}}

QPushButton:pressed {{
    border: none;
    background-color: {green};
}}
"""