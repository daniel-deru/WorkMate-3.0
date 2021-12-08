import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors


Calendar = f"""
    QCalendarWidget {{
        margin-top: 20px;
        background-color: {colors['background']};
        color: {colors['text']};
    }}
    QCalendarWidget QWidget {{
        background-color: {colors['background-active']};
        color: {colors['text-alt']};
    }}
    QCalendarWidget QTableView {{
        background-color: {colors['background-active']};
    }}
    QCalendarWidget QTableView QLabel {{
        color: {colors['text-alt']};
    }}

"""