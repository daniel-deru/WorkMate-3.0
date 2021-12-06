import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

Frame = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px;
        background-color: {colors['background']};
        color: {colors['text']};
        border: 2px solid {colors['border']};
    }}
"""

TodoFrameDelete = f"""
        QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: {colors['complete']};
        color: {colors['text']};
        max-height: 50px;
        height: 50px;
    }}
"""

TodoFrameComplete = f"""
    QFrame {{
        font-size: 16px;
        border-radius: 5px;
        font-size: 16px;
        background-color: {colors['incomplete']};
        color: {colors['text']};
        max-height: 50px;
        height: 50px;
    }}
"""