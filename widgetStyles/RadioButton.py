from msilib.schema import RadioButton
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default


RadioButton = f"""
    QRadioButton {{
        color: {default};
        font-size: 16px;
    }}

    QRadioButton::indicator:checked {{
        image: url(assets/radio-on.svg);
        max-height: 20px;
        max-width: 20px;
        height: 20px;
        width: 20px;
    }}

    QRadioButton::indicator:unchecked {{
        image: url(assets/radio-off.svg);
        max-height: 20px;
        max-width: 20px;
        height: 20px;
        width: 20px;
    }}
"""