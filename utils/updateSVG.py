import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

ASSETS_FOLDER = "assets/"
images = [
    f'{ASSETS_FOLDER}toggle-on.svg',
    f"{ASSETS_FOLDER}color_apps.svg",
    f"{ASSETS_FOLDER}color_vault.svg",
    f"{ASSETS_FOLDER}color_notes.svg",
    f"{ASSETS_FOLDER}color_task.svg",
    f"{ASSETS_FOLDER}color_settings.svg",
    f"{ASSETS_FOLDER}down-arrow.svg",
    f"{ASSETS_FOLDER}up-arrow.svg",
    f"{ASSETS_FOLDER}calendar.svg",
    f"{ASSETS_FOLDER}right-arrow.svg",
    f"{ASSETS_FOLDER}left-arrow.svg",
    f"{ASSETS_FOLDER}radio-on.svg"
    
]

def change_color(prevColor, newColor):
    data = None
    for image in images:      
        with open(image, 'r') as img:
            data = img.read()
            data = data.replace(prevColor, newColor)

        with open(image, 'w') as img:
            img.write(data)
