import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default

TableWidget = f"""
    QWidget {{
        padding: 0px;
    }}
    QTableWidget {{
        border: none;
        padding: 0px;
    }}
    QHeaderView {{
        qproperty-defaultAlignment: AlignHCenter AlignVCenter;
    }}
    QHeaderView::section {{
        padding: 5px; 
    }}
 
"""