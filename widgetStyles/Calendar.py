import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default


Calendar = f"""
    QCalendarWidget {{
        margin-top: 20px;
        background-color: {mode};
        color: {color};
    }}
    QCalendarWidget QWidget {{
        background-color: {color};
        color: {default};
    }}
    QCalendarWidget QTableView {{
        background-color: {color};
    }}
    QCalendarWidget QTableView QLabel {{
        color: {default};
    }}

"""