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
        padding: 0px 5px;
        width: 20px;
        font-size: 12px;
        border: none;
        background-color: {color};
    }}

    QComboBox::drop-down:pressed {{
        background-color: {mode};
    }}

    QComboBox QAbstractItemView {{
        background-color: {color};
        selection-background-color: {mode};
        selection-color: {default};
        color: {button};
        border-radius: 5px;
    }}
    QComboBox::down-arrow{{
        width: 15px;
        height: 15px;
        border: none;
        image: url(assets/down-arrow.svg);
    }}

    QComboBox QListView {{
        font-size: 5px
    }}
"""