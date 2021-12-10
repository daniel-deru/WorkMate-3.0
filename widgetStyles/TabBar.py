import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button

TabBar = f"""
    QTabBar{{
        background-color: {color};
    }}
   QTabBar::tab {{
        font-size: 16px;
        width: 100px;
        height: 30px;
        border: none;
        background-color: {color};
        color: {button};
    }}

        QTabBar::tab:selected {{
        background: {mode};
        color: {default};    
    }}
"""