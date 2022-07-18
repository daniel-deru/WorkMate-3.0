import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, green, orange
ScrollBar = f"""
   QScrollBar:vertical {{
                    width: 25px;
                    margin: 5px 0 5px 0;
                    background: {mode};
                  }}

                  QScrollBar::handle:vertical {{
                    border: 10px solid {color};
                    background: white;
                  }}

                  QScrollBar::add-line:vertical {{
                    background: none;
                    height: 5px;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                  }}

                  QScrollBar::sub-line:vertical {{
                    background: none;
                    height: 5px;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                  }}

                  QScrollBar::up-arrow:vertical {{
                    height: 5px; 
                    width: 5px 
                  }}

                  QScrollBar::down-arrow:vertical {{
                    height: 5px; 
                    width: 5px                    
                  }}
"""

VaultScrollBar = f"""
  QScrollBar {{
            border: 0px solid white;
            background: white;
            width: 5px;
            border-radius: 10px;    
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{         
            min-height: 0px;
          	border: 0px solid white;
			      border-radius: 10px;
			      background-color: {green};
        }}

"""