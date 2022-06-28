import os

development_mode = True

PATH = os.getenv("APPDATA") + "\\Smart WorkMate"

DB_PATH = PATH + "\\database\\"
if development_mode: DB_PATH = "./database/"

ASSET_PATH = "./assets/"

PICKLE_ENC = 'SqQ1-jsiAXjOmRWQqLWoMyzTWgW_Kxy8rc5aGKLG91k='
# ASSET_PATH = PATH + "\\assets"
