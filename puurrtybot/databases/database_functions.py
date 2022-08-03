import puurrtybot, json


def save_assets():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS, json_file)


def save_assets_addresses():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets_addresses.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS_ADDRESSES ,json_file)


def save_market_sales():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_sales.json""", 'w') as json_file:
        json.dump(puurrtybot.MARKET_SALES, json_file)


def save_market_sales_tx_hash():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_sales_tx_hash.json""", 'w') as json_file:
        json.dump(puurrtybot.MARKET_SALES_TX_HASH, json_file)


def save_market_listings():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_listings.json""", 'w') as json_file:
           json.dump(puurrtybot.MARKET_LISTINGS, json_file)


def save_market_listings_ids():
    with open(f"""{puurrtybot.DATABASES_DIR}/market_listings_ids.json""", 'w') as json_file:
        json.dump(puurrtybot.MARKET_LISTINGS_IDS, json_file)


def save_asset_sales_history():
    with open(f"""{puurrtybot.DATABASES_DIR}/assets_sales_history.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS_SALES_HISTORY, json_file)


def save_twitter_mentions():
    with open(f"""{puurrtybot.DATABASES_DIR}/twitter_mentions.json""", 'w') as json_file:
        json.dump(puurrtybot.TWITTER_MENTIONS ,json_file)


def save_users():
    with open(f"""{puurrtybot.DATABASES_DIR}/users.json""", 'w') as json_file:
        json.dump(puurrtybot.USERS ,json_file)