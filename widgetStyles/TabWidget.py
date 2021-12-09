import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

TabWidget = f"""
    QTabWidget {{
        background-color: {color};
    }}

    QTabWidget::pane {{
        border: none;
        background-color: {color};
    }}

    QTabWidget::tab-bar {{
        background-color: {color};
    }}
"""