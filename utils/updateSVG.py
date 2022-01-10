import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


images = [
    'assets/toggle-on.svg',
    "assets/color_apps.svg",
    "assets/color_vault.svg",
    "assets/color_notes.svg",
    "assets/color_task.svg",
    "assets/color_settings.svg"
]

def change_color(prevColor, newColor):
    data = None
    for image in images:      
        with open(image, 'r') as img:
            data = img.read()
            data = data.replace(prevColor, newColor)

        with open(image, 'w') as img:
            img.write(data)
