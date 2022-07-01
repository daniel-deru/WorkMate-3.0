import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

Widget = f"""
    QWidget {{
        font-size: 16px;
        padding: 5px 8px;
        background-color: {mode};
    }}
"""

MainWidget = f"""
    QWidget#main_container {{
        font-size: 16px;
        font-size: 16px;
        padding: 5px 8px;
        background-color: {color};
    }}
"""

TodoItemWidgetComplete = f"""
QWidget#TodoItem {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #ff0000;
        color: {color};
        max-height: 50px;
        height: 50px;
        border: 2px solid {color};
    }}
"""

TodoItemWidgetDelete = f"""
    QWidget#TodoItem {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: #00ff00;
        color: {color};
        max-height: 50px;
        height: 50px;
        border: 2px solid {color};
    }}
"""

SideWidget = f"""
    QWidget#sidewidget {{
        background-image: url(:/other/background.jpg);
    }}

"""