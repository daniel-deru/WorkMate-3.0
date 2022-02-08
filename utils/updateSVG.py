import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.globals import ASSET_PATH
# PATH = "assets/"
images = [
    f'{ASSET_PATH}/toggle-on.svg',
    f"{ASSET_PATH}/color_apps.svg",
    f"{ASSET_PATH}/color_vault.svg",
    f"{ASSET_PATH}/color_notes.svg",
    f"{ASSET_PATH}/color_task.svg",
    f"{ASSET_PATH}/color_settings.svg",
    f"{ASSET_PATH}/down-arrow.svg",
    f"{ASSET_PATH}/up-arrow.svg",
    f"{ASSET_PATH}/calendar.svg",
    f"{ASSET_PATH}/right-arrow.svg",
    f"{ASSET_PATH}/left-arrow.svg",
    f"{ASSET_PATH}/radio-on.svg"
    
]

def change_color(prevColor, newColor):
    data = None
    for image in images:      
        with open(image, 'r') as img:
            data = img.read()
            data = data.replace(prevColor, newColor)

        with open(image, 'w') as img:
            img.write(data)
