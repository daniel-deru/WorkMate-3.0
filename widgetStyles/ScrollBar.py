ScrollBar = f"""
    QScrollBar:vertical {{
        width: 45px;
        margin: 45px 0 45px 0;
    }}

    QScrollBar::handle:vertical {{
        min-height: 10px;
    }}

    QScrollBar::add-line:vertical {{
        background: none;
        height: 45px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}

    QScrollBar::sub-line:vertical {{
        background: none;
        height: 45px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}
"""