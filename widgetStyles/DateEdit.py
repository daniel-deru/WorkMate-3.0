import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

DateEdit = f"""
    QDateEdit {{
        border: none;
    }}
    QDateEdit::drop-down {{
        background-color: {colors['background-active']};
        color: {colors['text-alt']};
        padding: 5px;
        border-radius: 5px;
        width: 40px;
        image: url(assets/calendar.png);
    }}
"""