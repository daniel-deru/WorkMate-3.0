import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from styles.styles import colors

Dialog = f"""
    QDialog {{
        background-color: {colors['background']};
        font-size: 16px;
    }}
"""