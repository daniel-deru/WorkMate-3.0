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
}}

QPushButton:pressed {{
    background-color: transparent;
    color: {default};
    border: 2px solid {light_blue};
}}
"""

ForgotPasswordButton = f"""
    QPushButton#btn_forgot_password {{
        max-width: 1000000px;
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
    background-color: #051456;
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
