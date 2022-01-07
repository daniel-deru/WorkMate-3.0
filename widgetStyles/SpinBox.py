import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

SpinBox = f"""
    QSpinBox {{
        background-color: {mode};
        color: {default};
        font-size: 16px;
        padding: 5px 8px;
        border-radius: 5px;
        border: 2px solid {color};
    }}

    QSpinBox::down-button {{
        border: none;
        image: url(assets/down-arrow.svg);
        margin-top: 2px;
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        background-color: {color};
    }}

    QSpinBox::up-button:pressed {{
        background-color: {mode};
    }}

    QSpinBox::up-button {{
        border: none;
        image: url(assets/up-arrow.svg);
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        margin-bottom: 2px;
        background-color: {color};
    }}

    QSpinBox::down-button:pressed {{
        background-color: {mode};
    }}

"""