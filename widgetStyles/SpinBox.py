import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default
from utils.globals import ASSET_PATH

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
        border-left: 2px solid {color};
        image: url({ASSET_PATH}down-arrow.svg);
        margin-top: 2px;
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        background-color: {mode};
    }}

    QSpinBox::up-button:pressed {{
        background-color: {mode};
    }}

    QSpinBox::up-button {{
        border: none;
        border-left: 2px solid {color};
        image: url({ASSET_PATH}up-arrow.svg);
        width: 15px;
        height: 15px;
        padding: 0px 5px;
        margin-bottom: 2px;
        background-color: {mode};
    }}

    QSpinBox::down-button:pressed {{
        background-color: {mode};
    }}

"""