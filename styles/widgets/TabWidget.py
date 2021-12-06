import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

TabWidget = f"""
    QTabWidget {{
        background-color: {colors['background-active']};
    }}

    QTabWidget::pane {{
        border: none;
        background-color: {colors['background-active']};
    }}

    QTabWidget::tab-bar {{
        background-color: {colors['background-active']};
    }}
"""