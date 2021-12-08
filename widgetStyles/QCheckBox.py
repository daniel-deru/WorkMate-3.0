import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

CheckBox = f"""
    QCheckBox {{
        color: {colors['text']};
        font-size: 16px;
        border-radius: 5px;
    }}

    QCheckBox::indicator:checked {{
        image: url(assets/check-on.png);
    }}

    QCheckBox::indicator{{
        image: url(assets/check-off.png);
        width: 50px;
        height: 25px;
        max-width: 50px;
        max-height: 25px;
    }}

"""