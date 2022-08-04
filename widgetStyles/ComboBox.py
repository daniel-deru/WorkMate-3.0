from widgetStyles.styles import default, mode, button, color, dark_blue, light_blue, green
import assets.resources

ComboBox = f"""
    QComboBox {{
        color: {default};
        border: 2px solid {light_blue};
        background-color: {mode};
        border-radius: 5px;
        font-size: 16px;
    }}

    QComboBox::drop-down {{
        width: 40px;
        background-color: {mode};
 
    }}

    QComboBox QAbstractItemView {{
        background-color: {mode};
        selection-background-color: {green};
        selection-color: {default};
        color: {default};
        outline: none;
        padding: 0px;
        border: 2px solid {light_blue};
    }}
    
    QComboBox QAbstractItemView::item {{
        min-height: 35px;
    }}
    
    QComboBox QAbstractItemView::item:selected {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox QAbstractItemView::item:hover {{
        background-color: {green};
        color: black;
    }}
    
    QComboBox::down-arrow{{
        width: 15px;
        height: 15px;
        background-color: {mode};
        image: url(:/arrows/down-arrow.svg);
    }} 
"""