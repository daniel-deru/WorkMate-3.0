import math
import sys
import os
import re
from functools import reduce

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

from widgetStyles.styles import placeholders
from database.model import Model

# clears the window so it can be repainted
def clear_window(container):
    # This is to remove the previous widgets that were painted so the widgets don't get added twice
    prevItems = container.count()
    # check if there are widgets
    if prevItems > 0:
        for i in range(container.count()):
            item = container.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.spacerItem():
                container.removeItem(item.spacerItem())


def display_grid():
    pass
 

class StyleSheet():
    def __init__(self, stylesheet):
        self.stylesheet = stylesheet
        settings = Model().read("settings")[0]
        self.settings_mode = "#000000" if settings[1] else "#ffffff"
        self.settings_contrast = "#ffffff" if settings[1] else  "#000000"
        self.settings_color = settings[3]

    def rgb(self, color):
        color /= 255
        if color <= 0.03928:
            return color / 12.92
        else:
            return math.pow( (color + 0.055) / 1.055, 2.4)

    def luminance(self, hex):
        r = int(hex[1:3], 16)
        g = int(hex[3:5], 16)
        b = int(hex[5:7], 16)
        array = list(map(self.rgb, [r, g, b]))
        return round( (array[0] * 0.2126 + array[1] * 0.7152 + array[2] * 0.0722), 4 )


    def contrast(self, c1, c2):
        color1 = self.luminance(c1)
        color2 = self.luminance(c2)
        if color1 > color2:
            return round((color1 + 0.05) / (color2 + 0.05), 1)
        elif color2 > color1:
            return round((color2 + 0.05) / (color1 + 0.05), 1)
        else:
            return 1
    
    def create(self):
        black_contrast = self.contrast(self.settings_color, "#000000")
        white_contrast = self.contrast(self.settings_color, "#ffffff")
        color_contrast = self.contrast(self.settings_color, self.settings_mode)


        settings_button = "#000000" if black_contrast > white_contrast else "#ffffff"
        settings_default = self.settings_contrast if color_contrast < 3 else self.settings_color
        # settings_default = self.settings_contrast

        values = [self.settings_color, self.settings_mode, settings_default, settings_button]

        stylesheet = reduce(lambda a, b: a + b, self.stylesheet)
        for i in range(len(placeholders)):
            stylesheet = re.sub(placeholders[i], values[i], stylesheet)
        return stylesheet

def import_file(table, file):
    pass
        
