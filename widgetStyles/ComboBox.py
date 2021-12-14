from widgetStyles.styles import default, mode, button, color

ComboBox = f"""
    QComboBox {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        color: {default};
        border: 2px solid {color};
        background-color: {mode};
        border-radius: 5px;
        padding: 5px;
    }}

    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        color: white;
        padding-left: 5px;
        font-size: 12px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {color};
        selection-background-color: {mode};
        selection-color: {default};
        color: {button};
        border-radius: 5px;
    }}
    QComboBox::down-arrow{{
        width: 7px;
        height: 5px;
        border: none;
        background-color: {color};
    }}
"""