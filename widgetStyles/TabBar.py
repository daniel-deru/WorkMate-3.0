import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button

TabBar = f"""
    QTabBar{{
        background-color: {color};
        border: none;
        qproperty-drawBase: 0;
    }}
   QTabBar::tab {{
        font-size: 16px;
        width: 100px;
        height: 40px;
        border: none;
        background-color: {color};
        color: {button};
        padding-left: 15px;
    }}

        QTabBar::tab:selected {{
        background: {mode};
        color: {default};    
    }}
"""