import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

TabBar = f"""
   QTabBar::tab {{
        font-size: 16px;
        width: 100px;
        height: 30px;
        border: none;
        background: {colors['background-active']};
        color: {colors['background']};
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }}

        QTabBar::tab:selected {{
        background: {colors['background']};
        color: {colors['text']};
        border-radius: 0px;
        
    }}
"""