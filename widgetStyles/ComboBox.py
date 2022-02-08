from widgetStyles.styles import default, mode, button, color, dark_blue, light_blue, green
from utils.globals import ASSET_PATH

ComboBox = f"""
    QComboBox {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        color: {default};
        border: 2px solid {dark_blue};
        background-color: {mode};
        border-radius: 5px;
        padding: 5px;
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        color: white;
        padding: 0px 5px;
        width: 20px;
        font-size: 12px;
        border: none;
        border-left: 2px solid {dark_blue};
        background-color: {mode};
    }}

    QComboBox::drop-down:pressed {{
        background-color: {mode};
    }}

    QComboBox QAbstractItemView {{
        background-color: {dark_blue};
        selection-background-color: {mode};
        selection-color: {default};
        color: {button};
        border-radius: 5px;
    }}
    QComboBox::down-arrow{{
        width: 15px;
        height: 15px;
        border: none;
        background-color: {mode};
        image: url({ASSET_PATH}down-arrow.svg);
    }}

    QComboBox QListView {{
        font-size: 5px
    }}
"""