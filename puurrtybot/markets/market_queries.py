import os, puurrtybot, requests, datetime, puurrtybot.functions as pf, puurrtybot.databases.database_functions as ddf


def get_untracked_sales_jpgstore():
    page = 1
    last_sale = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page={page}&count=1""").json()
    untracked_sales = []

    try:
        puurrtybot.MARKET_SALES_TX_HASH[last_sale['transactions'][0]['tx_hash']]
    except KeyError:
        untracked = True
        while untracked:
            sales = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page={page}&count=10""").json()['transactions']
            for sale in sales:
                try:
                    puurrtybot.MARKET_SALES_TX_HASH[sale['tx_hash']]
                    untracked = False
                    break;
                except KeyError:
                    untracked_sales.append(sale)
            page+=1

        for i,sale in enumerate(untracked_sales):
            if sale['action'] in ['BUY','ACCEPT_OFFER']:
                timestamp = pf.time_to_timestamp(sale['confirmed_at'].split('.')[0].split('+')[0].replace('T',' '))
                amount = int(sale['amount_lovelace'])/1_000_000
                untracked_sales[i] = {'tx_hash':sale['tx_hash'], 'timestamp':timestamp, 'asset':sale['asset_id'], 'amount':amount, 'market':'jpgstore'}
                puurrtybot.MARKET_SALES_TX_HASH[sale['tx_hash']] = True
                try:
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['amounts'].append(amount)
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['timestamps'].append(timestamp)
                except KeyError:
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset']] = {}
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['amounts'] =  [amount]
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset']]['timestamps'] =  [timestamp]
            else:
                del untracked_sales[i]

        ddf.save_asset_sales_history()
        ddf.save_market_sale()
    return untracked_sales



def check_sales(ctx):
    market_last_100 = requests.get("""https://server.jpgstoreapis.com/collection/f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e/transactions?page=1&count=100""").json()
    buy_path = puurrtybot.PATH/"puurrtybot/databases/market_buys"
    past_buys = os.listdir(buy_path)


    one_sell = False
    for move in market_last_100['transactions'][::-1]:
        if move['tx_hash'] not in past_buys:
            if move['action']=='BUY':
                timestamp = int(datetime.datetime.strptime(move['confirmed_at'].replace('T',' ').split('+',1)[0].split('.',1)[0], '%Y-%m-%d %H:%M:%S').timestamp())
                if timestamp - int(datetime.datetime.utcnow().timestamp()) + 70*60 > 0:
                    # timestamp
                    ada = move['amount_lovelace']/1_000_000
                    asset = move['asset_id']
                    meta_name = move['display_name']
                    ctx.send(f"""{meta_name} sold for {ada} at <t:{timestamp}:f>.""")
                    with open(f"""{buy_path}/{move['tx_hash']}""", 'w') as f:
                        f.write('')
                    one_sell = True
    if not one_sell:
        ctx.send(f"""No new sales""")