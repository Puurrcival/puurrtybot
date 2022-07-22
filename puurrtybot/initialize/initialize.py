import puurrtybot, json, requests, tqdm, os
import puurrtybot.blockfrost.blockfrost_queries as bbq
import puurrtybot.twitter.twitter_queries as ttq
import puurrtybot.functions as pf


def delete_file(PATH):
    try:
        os.unlink(PATH)
    except FileNotFoundError:
        pass


def initialize_assets_json():
    puurrtybot.ASSETS = {}
    for asset in tqdm.tqdm(bbq.get_asset_list_by_policy(policy = puurrtybot.POLICY)):
        puurrtybot.ASSETS[asset] = bbq.get_meta_by_asset(asset)
    with open(f"""{puurrtybot.DATABASES_DIR}/assets.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS, json_file)


def initialize_market_sales_json():
    # jpgstore
    jpgstore_sales = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page=1&count=100000""").json()['transactions']
    for i, sale in enumerate(jpgstore_sales):
        if sale['action'] in ['BUY','ACCEPT_OFFER']:
            timestamp = pf.time_to_timestamp(sale['confirmed_at'].split('.')[0].split('+')[0].replace('T',' '))
            jpgstore_sales[i] = {'tx_hash':sale['tx_hash'], 'timestamp':timestamp, 'asset':sale['asset_id'], 'amount':int(sale['amount_lovelace'])/1_000_000, 'market':'jpgstore'}
        else:
            del jpgstore_sales[i]
    puurrtybot.MARKET_SALES = sorted(jpgstore_sales, key=lambda d: d['timestamp'], reverse=True)
    with open(f"""{puurrtybot.DATABASES_DIR}/market_sales.json""", 'w') as json_file:
            json.dump(puurrtybot.MARKET_SALES, json_file)


def initialize_asset_sales_history_json():
    puurrtybot.ASSETS_SALES_HISTORY = {}
    for sale in puurrtybot.MARKET_SALES:
        try:
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']].append(sale['amount'])
        except KeyError:
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']] =  [sale['amount']]
    with open(f"""{puurrtybot.DATABASES_DIR}/assets_sales_history.json""", 'w') as json_file:
        json.dump(puurrtybot.ASSETS_SALES_HISTORY, json_file)


def initialize_twitter_mentions():
    puurrtybot.TWITTER_MENTIONS = {}
    try:
        tweets = ttq.get_mentions_puurrtycats()['data']
        for tweet in tweets:
            puurrtybot.TWITTER_MENTIONS[tweet['id']] = tweet
    except KeyError:
        pass
    with open(f"""{puurrtybot.DATABASES_DIR}/twitter_mentions.json""", 'w') as json_file:
        json.dump(puurrtybot.TWITTER_MENTIONS, json_file)


def initialize_databases():
    #initialize_assets_json()
    initialize_market_sales_json()
    initialize_asset_sales_history_json()
    initialize_twitter_mentions()

initialize_databases()