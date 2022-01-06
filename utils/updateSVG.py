import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


images = [
    'assets/check-on.svg',
    'assets/color_splash.svg'
]

def change_color(prevColor, newColor):
    print(prevColor, newColor)
    data = None
    for image in images:      
        with open(image, 'r') as img:
            data = img.read()
            data = data.replace(prevColor, newColor)

        with open(image, 'w') as img:
            img.write(data)
