from pathlib import Path
import json, tqdm, os

PATH = Path(__file__).parent.parent
DATABASES_DIR = f"""{PATH}/puurrtybot/databases"""
USERS_DIR = f"""{PATH}/puurrtybot/databases/users"""


GUILD = 998148160243384321
ROLES = []


ROLES_ACCESS = {
        998185453083705425: "Admin", # Admins
        998186644836470806: "Bot", # Bots
        1001480465259175947: "verified", #verified member 
        }


ROLES_N = {
        998190425275904000:   ("Stray Cat", 0), # 0 cats
        998571659382505492:   ("Puurrty Cat", 1), # 1 cat
        1001479213062299709:  ("Puurrty Puurrson", 2), # 2-4 cats
        1001479154555953202:  ("Puurrty Lovuurr", 5), # 5-9 cats
        1001479010167038043:  ("Puurrty Hoarduurr", 10), # 10-24 cats
        1001478933528723506:  ("Puurrty 25+", 25), # 25-49 cats
        1001478852020797521:  ("Puurrty 50+", 50), # 50-79 cats
        1001478797595517018:  ("Puurrty 80+", 80), # 80-124 cats
        1001478314013229208:  ("Puurrty 125+", 125), # 125-174 cats
        1001478244752699482:  ("Puurrty 200+", 175), # 175-349 cats
        1001478112602763335:  ("Puurrty 350+", 350), # 350-699 cats
        1001477747866075216:  ("Puurrty 700+", 700) # 700+ cats
        }


ROLES_N_DICT = {v[1]:k for k, v in ROLES_N.items()}


ROLES_TRAITS = {
        "Kitsune": 1001838062667579456,
        "Zombie":  1001838223263281152,
        "Wizard":  1001838343216181258,
        "Angel": 1002193337408835605,
        "Crystal": 1002193227975250050,
        "Cyborg": 1002193140452692068,
        "Devil": 1002193053576085534,
        "Gold": 1002192993589133402,
        "Jason": 1002192909107482765,
        "Royal": 1002192837066117150,
        "Unique": 1002192667410710639,
        "Pirate": 1002195354051166270,
        "Skeleton": 1002192551081693226,
        "Laser": 1001982288042655825,
        "Educated": 1002563315509248110,
        }

JOIN_TRAITS = {
    #kitsune
    "Kitsune": "kitsune",

    #zombie
    "Zombie": "zombie",

    #wizard
    "Wizard Hat": "wizard", 
    "Wizard Robe": "wizard",
    "Wand": "wizard",

    #angel
    "Halo": "angel",
    "Angel Wings": "angel",

    #crystal
    "Crystal": "crystal",

    #cyborg
    "Cyborg": "cyborg",

    #devil
    "Devil": "devil",
    "Fire Eyes": "devil",
    "Devil Tail": "devil",

    #gold
    "Gold": "gold",

    #jason
    "Jason": "jason",

    #royal
    "Crown": "royal", 
    "Pharaoh Headress": "royal",
    "Royal Cloak": "royal",

    #unique
    "Yes": "unique",

    #pirate                     
    "Pirate Hat": "pirate",
    "Pirate Jacket": "pirate",

    #skeleton
    "Skeleton": "skeleton",

    #laser
    "Laser Eyes": "laser",

    #laser
    "Professor": "educated",
    "Dr.": "educated",
    "Ph.D.": "educated",
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
MARKET_SALES_TX_HASH = load_json_db('market_sales_tx_hash')
ASSETS_SALES_HISTORY = load_json_db('assets_sales_history')
TWITTER_MENTIONS = load_json_db('twitter_mentions')

USERS =  {}
for user_json in tqdm.tqdm(os.listdir(USERS_DIR)):
    with open(f"""{USERS_DIR}/{user_json}""", 'r') as openfile:
        user = json.load(openfile)
    USERS.update(user)