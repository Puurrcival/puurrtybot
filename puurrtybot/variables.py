from pathlib import Path
import json, tqdm, os

PATH = Path(__file__).parent.parent
DATABASES_DIR = f"""{PATH}/puurrtybot/databases"""
USERS_DIR = f"""{PATH}/puurrtybot/databases/users"""


ROLES = {
        998185453083705425: "Admin", # Admins
        998186644836470806: "Bot", # Bots
        1001480465259175947: "verified", #verified member 
        998190425275904000: "Stray Cat", # 0 cats
        998571659382505492: "Puurrty Cat", # 1 cat
        1001479213062299709 : "Puurrty Puurrson", # 2-4 cats
        1001479154555953202 : "Puurrty Lovuurr", # 5-9 cats
        1001479010167038043 : "Puurrty Hoarduurr", # 10-24 cats
        1001478933528723506 : "Puurrty 25+", # 25-49 cats
        1001478852020797521 : "Puurrty 50+", # 50-79 cats
        1001478797595517018 : "Puurrty 80+", # 80-124 cats
        1001478314013229208 : "Puurrty 125+", # 125-174 cats
        1001478244752699482 : "Puurrty 200+", # 175-349 cats
        1001478112602763335 : "Puurrty 350+", # 350-699 cats
        1001477747866075216 : "Puurrty 700+" # 700+ cats
        }


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
MARKET_SALES_TX_HASH = {sale['tx_hash']:True for sale in MARKET_SALES}
ASSETS_SALES_HISTORY = load_json_db('assets_sales_history')
TWITTER_MENTIONS = load_json_db('twitter_mentions')

USERS =  {}
for user_json in tqdm.tqdm(os.listdir(USERS_DIR)):
    with open(f"""{USERS_DIR}/{user_json}""", 'r') as openfile:
        user = json.load(openfile)
    USERS.update(user)