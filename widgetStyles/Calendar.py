import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from widgetStyles.styles import color, mode, default, button
from utils.globals import ASSET_PATH


Calendar = f"""
QCalendarWidget {{
    border: 2px solid {color};
}}
QCalendarWidget QToolButton {{
  	height: 40px;
  	width: 100px;
  	color: {button};
  	font-size: 16px;
  	icon-size: 37px, 37px;
  	background-color: {color};
  }}


  QCalendarWidget QWidget#qt_calendar_prevmonth {{
      qproperty-icon: url({ASSET_PATH}left-arrow.svg);
      background-color: {mode};
      border-left: 2px solid {color};
      border-top: 2px solid {color}
  }}
  QCalendarWidget QWidget#qt_calendar_nextmonth {{
      qproperty-icon: url({ASSET_PATH}right-arrow.svg);
      background-color: {mode};
      border-right: 2px solid {color};
      border-top: 2px solid {color}
  }}


  QCalendarWidget QMenu {{
  	width: 100px;
  	left: 20px;
  	color: {color};
  	font-size: 12px;
  	background-color: {mode};
  }}

  QCalendarWidget QSpinBox {{ 
  	width: 100px; 
  	font-size:16px; 
  	color: {color}; 
  	background-color: {mode}; 
  	selection-background-color: {color};
  	selection-color: {button};
  }}

    QCalendarWidget QSpinBox::up-button {{ 
        subcontrol-origin: border;  
        subcontrol-position: top right;  
        image: url({ASSET_PATH}up-arrow.svg);
        width: 30px;
        height: 30px; 
    }}

    QCalendarWidget QSpinBox::down-button {{
        subcontrol-origin: border; 
        subcontrol-position: bottom right;  
        image: url({ASSET_PATH}down-arrow.svg);
        width: 30px;  
        height: 30px; 
    }}

    QCalendarWidget QSpinBox::up-arrow {{ 
        width: 10px;  
        height: 10px; 
    }}

    QCalendarWidget QSpinBox::down-arrow {{ 
        width: 10px;  
        height: 10px;
    }}
   

    QCalendarWidget QWidget {{ 
        alternate-background-color: {mode};
        }}
   
    QCalendarWidget QAbstractItemView:enabled {{
        font-size: 16px;  
        color: {color};  
        background-color: {mode};  
        selection-background-color: {color}; 
        selection-color: {button};
        outline: none;
        padding: 10px;
        border-bottom: 2px solid {color};
        border-left: 2px solid {color};
        border-right: 2px solid {color};

    }}
   

    QCalendarWidget QAbstractItemView:disabled {{ 
        color: {color}; 
    }}
"""