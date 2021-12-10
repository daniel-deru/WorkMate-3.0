import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

DateEdit = f"""
    QDateEdit {{
        border: none;
        color: {default};
    }}
    QDateEdit::drop-down {{
        background-color: {color};
        color: {default};
        padding: 5px;
        border-radius: 5px;
        width: 40px;
        image: url(assets/calendar.png);
    }}
"""