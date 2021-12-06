import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

DateEdit = f"""
    QDateEdit::drop-down {{
        border: 2px solid {colors['text']};
        background-color: {colors['background']};
        color: {colors['text']};
        padding: 5px;
        border-radius: 5px;
        width: 40px;
        image: url(assets/calendar.png);
    }}
"""