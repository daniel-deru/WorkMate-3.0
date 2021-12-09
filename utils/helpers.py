import math  

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
 

class Contrast():
    def __init__(self, c1, c2):
        self.c1 =c1
        self.c2 =c2

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


    def contrast(self):
        color1 = self.luminance(self.c1)
        color2 = self.luminance(self.c2)
        if color1 > color2:
            return round((color1 + 0.05) / (color2 + 0.05), 1)
        elif color2 > color1:
            return round((color2 + 0.05) / (color1 + 0.05), 1)
        else:
            return 1