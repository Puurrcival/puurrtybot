from pathlib import Path
import json, tqdm, os

PATH = Path(__file__).parent.parent
DATABASES_DIR = f"""{PATH}/puurrtybot/databases"""


GUILD = 998148160243384321
TWITTER_ID = 1479912806866694149 #PuurrtyCats
ROLES = None
SESSION = None


def load_json_db(DB_PATH: str):
    try:
        with open(f"""{DATABASES_DIR}/{DB_PATH}.json""", 'r') as json_file:
            DB = json.load(json_file)
    except FileNotFoundError:
        DB = {}
    return DB

ASSETS = load_json_db('assets')
ASSETS_ADDRESSES = load_json_db('assets_addresses')
MARKET_SALES = load_json_db('market_sales')
MARKET_SALES_TX_HASH = load_json_db('market_sales_tx_hash')
MARKET_LISTINGS = load_json_db('market_listings')
MARKET_LISTINGS_IDS = load_json_db('market_listings_ids')
ASSETS_SALES_HISTORY = load_json_db('assets_sales_history')
TWITTER_MENTIONS = load_json_db('twitter_mentions')