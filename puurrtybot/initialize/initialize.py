import puurrtybot, json, requests
import puurrtybot.blockfrost.blockfrost_queries as bbq


def initialize_assets_json():
    puurrtybot.ASSETS = {asset:bbq.get_meta_by_asset(asset) in bbq.get_asset_list_by_policy(policy = puurrtybot.POLICY)}
    with open(f"""{puurrtybot.DATABASES_DIR}/assets.json""", 'w') as f:
        json.dump(puurrtybot.ASSETS, f)


def initialize_market_sales_json():
    puurrtybot.MARKET_SALES = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page=1&count=100000""").json()['transactions']
    puurrtybot.MARKET_SALES = [sale for sale in puurrtybot.MARKET_SALES if sale['action'] in ['BUY', 'ACCEPT_OFFER']]
    with open(f"""{puurrtybot.DATABASES_DIR}/sales.json""", 'w') as f:
        json.dump(puurrtybot.MARKET_SALES, f)
