import puurrtybot, requests, puurrtybot.functions as pf, puurrtybot.databases.database_functions as ddf


def get_untracked_sales_jpgstore():
    page = 1
    last_sale = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page={page}&count=1""").json()
    untracked_sales = {}

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
                    untracked_sales[sale['tx_hash']]= sale
            page+=1

        for tx_hash,sale in list(untracked_sales.items())[::-1]:
            if sale['action'] in ['BUY','ACCEPT_OFFER'] and sale['confirmed_at']:
                timestamp = pf.time_to_timestamp(sale['confirmed_at'].split('.')[0].split('+')[0].replace('T',' '))
                amount = int(sale['amount_lovelace'])/1_000_000
                untracked_sales[tx_hash] = {'tx_hash':sale['tx_hash'], 'timestamp':timestamp, 'asset':sale['asset_id'], 'amount':amount, 'market':'jpgstore'}
                puurrtybot.MARKET_SALES_TX_HASH[sale['tx_hash']] = True
                try:
                    print('try saving', amount, sale['asset_id'])
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset_id']]['amounts'].append(amount)
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset_id']]['timestamps'].append(timestamp)
                except KeyError:
                    print('except saving', amount, sale['asset_id'])
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset_id']] = {}
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset_id']]['amounts'] =  [amount]
                    puurrtybot.ASSETS_SALES_HISTORY[sale['asset_id']]['timestamps'] =  [timestamp]
            else:
                untracked_sales[tx_hash] = None
        untracked_sales = [sale for _, sale in untracked_sales.items() if sale]
        if untracked_sales:
            ddf.save_asset_sales_history()
            ddf.save_market_sales()
            ddf.save_market_sales_tx_hash()
            return sorted(untracked_sales, key=lambda sales: sales['timestamp'], reverse=False)
    return untracked_sales