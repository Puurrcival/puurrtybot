import os, puurrtybot, requests, datetime

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