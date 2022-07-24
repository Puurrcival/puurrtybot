import puurrtybot, json, requests, tqdm, os
import puurrtybot.blockfrost.blockfrost_queries as bbq
import puurrtybot.twitter.twitter_queries as ttq
import puurrtybot.functions as pf
import puurrtybot.databases.database_functions as ddf


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
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['amounts'].append(sale['amount'])
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['timestamps'].append(sale['timestamp'])
        except KeyError:
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']] = {}
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['amounts'] =  [sale['amount']]
            puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['timestamps'] =  [sale['timestamp']]
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


def get_mint_price(amount):
    amount = int(int(amount)/1_000_000)
    if amount%52==0:
        return 52
    if amount%62==0:
        return 62
    if amount%72==0:
        return 72
    if amount%82==0:
        return 82
    if amount%92==0:
        return 92
    if amount%100==0:
        return 100
    if amount==5:
        return 1
    return amount


def initialize_mint_prices(mint_address = 'addr1vxk4szdzv6qxqne5k3m0wr4m5cewh2pnt23tn3tx2x28zsq7ml8dm'):
    mint_tx_hash_list = bbq.get_tx_hash_list_by_address(mint_address, order="asc", past_time = bbq.get_server_time(), hash_only=False)
    quantity_inputs = {}
    for tx in tqdm.tqdm(mint_tx_hash_list):
        block_time = tx['block_time']
        utxo_list = bbq.get_utxo_list_by_tx_hash(tx['tx_hash'])
        inputs = [utxo['address'] for utxo in utxo_list['inputs']]
        outputs = [utxo['amount'][0]['quantity'] for utxo in utxo_list['outputs'] if utxo['address']==mint_address]
        if outputs:
            quantity_inputs[tx['tx_hash']] = {'block_time':block_time, 'input_addresses': inputs, 'quantities': outputs}

    mint_matches = {}
    for asset in tqdm.tqdm(puurrtybot.ASSETS.keys()):
        mint_tx_hash = puurrtybot.ASSETS[asset]["initial_mint_tx_hash"]
        utxo_list = bbq.get_utxo_list_by_tx_hash(mint_tx_hash)
        mint_address = [utxo['address']  for utxo in utxo_list['outputs'] if [amount for amount in utxo['amount'] if asset == amount['unit']]][0]
        mint_block_time = bbq.get_tx_by_tx_hash(mint_tx_hash)['block_time']
        for _ , data in quantity_inputs.items():
            if data['block_time'] < mint_block_time and mint_address in data['input_addresses']:
                try:
                    mint_matches[asset] += [{'mint_block_time': mint_block_time,'block_time': data['block_time'], 'address': mint_address, 'quantity':data['quantities']}]
                except KeyError:
                    mint_matches[asset] = [{'mint_block_time': mint_block_time,'block_time': data['block_time'], 'address': mint_address, 'quantity':data['quantities']}]
        try:
            mint_matches[asset]
        except KeyError:
            mint_matches[asset] = mint_block_time

    for asset, data in mint_matches.items():
        if type(data) != int:
            puurrtybot.ASSETS[asset]['mint_price'] = [get_mint_price(d['quantity'][0]) for d in data][-1]
            puurrtybot.ASSETS[asset]['mint_time'] = data[0]['mint_block_time']
        else:
            puurrtybot.ASSETS[asset]['mint_price'] = 0
            puurrtybot.ASSETS[asset]['mint_time'] = data
    ddf.save_assets()

def initialize_databases():
    #initialize_assets_json()
    #initialize_mint_prices()
    initialize_market_sales_json()
    initialize_asset_sales_history_json()
    initialize_twitter_mentions()

initialize_databases()