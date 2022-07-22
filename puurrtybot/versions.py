from pathlib import Path
import json

PATH = Path(__file__).parent.parent

VERSION = "Alpha"

POLICY = "f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e"

DATABASES_DIR = f"""{PATH}/puurrtybot/databases"""


def load_json_db(DB_PATH: str):
    try:
        with open(f"""{DATABASES_DIR}/{DB_PATH}.json""", 'r') as json_file:
            DB = json.load(json_file)
    except FileNotFoundError:
        DB = {}
    return DB


ASSETS = load_json_db('assets')
MARKET_SALES = load_json_db('market_sales')
MARKET_SALES_TX_HASH = {sale['tx_hash']:True for sale in MARKET_SALES}
ASSETS_SALES_HISTORY = load_json_db('assets_sales_history')
TWITTER_MENTIONS = load_json_db('twitter_mentions')