import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button, green, orange, light_blue, dark_blue

TabBar = f"""
    QTabBar{{
        background-color: {green};
        border: none;
        qproperty-drawBase: 0;
    }}
   QTabBar::tab {{
        font-size: 16px;
        width: 100px;
        height: 40px;
        border: none;
        background-color: {green};
        color: {dark_blue};
        padding-left: 15px;
    }}

        QTabBar::tab:selected {{
        background: {mode};
        color: {dark_blue};    
    }}
"""