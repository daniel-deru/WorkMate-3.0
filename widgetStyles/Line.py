import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, green


Line = f"""
    QFrame::Sunken {{
        border: 2px solid {green};
    }}

    QFrame[frameShape="5"] {{
        border: 2px solid {green};
    }}
    
    QFrame[frameShape="4"] {{
        border: 2px solid {green};
    }}

"""