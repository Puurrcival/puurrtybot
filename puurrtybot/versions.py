from pathlib import Path
import json

PATH = Path(__file__).parent.parent

VERSION = "Alpha"

POLICY = "f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e"

DATABASES_DIR = f"""{PATH}/puurrtybot/databases"""

try:
    with open(f"""{DATABASES_DIR}/assets.json""", 'r') as json_file:
        ASSETS = json.load(json_file)
except FileNotFoundError:
    ASSETS = {}


try:
    with open(f"""{DATABASES_DIR}/sales.json""", 'r') as json_file:
        MARKET_SALES = json.load(json_file)
except FileNotFoundError:
    MARKET_SALES = {}