import puurrtybot, requests, puurrtybot.functions as pf, puurrtybot.databases.database_functions as ddf

import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi


def get_untracked_sales_jpgstore():
    page = 1
    last_sale = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page={page}&count=1""").json()
    untracked_sales = {}


    if not ddq.get_sale_by_tx_hash(last_sale['transactions'][0]['tx_hash']):
        untracked = True
        while untracked:
            sales = requests.get(f"""https://server.jpgstoreapis.com/collection/{puurrtybot.POLICY}/transactions?page={page}&count=10""").json()['transactions']
            for sale in sales:
                if ddq.get_sale_by_tx_hash(sale['tx_hash']):
                    untracked = False
                    break;
                else:
                    untracked_sales[sale['tx_hash']] = sale
            page+=1

        for _ ,sale in list(untracked_sales.items())[::-1]:
            if sale['action'] in ['BUY','ACCEPT_OFFER'] and sale['confirmed_at']:
                timestamp = pf.time_to_timestamp(sale['confirmed_at'].split('.')[0].split('+')[0].replace('T',' '))
                ddi.sale_new(tx_hash = sale['tx_hash'] ,asset_id=sale['asset_id'], timestamp = timestamp, amount = int(sale['amount_lovelace']))


def get_untracked_listings_jpgstore():
    last_listing = requests.get(f"""https://server.jpgstoreapis.com/search/tokens?policyIds=[%22{puurrtybot.POLICY}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size=1""").json()['tokens'][0]
    untracked_listings = {}

    if not ddq.get_listing_by_id(f"""{last_listing['listed_at']}_{last_listing['asset_name']}"""):
        listings = requests.get(f"""https://server.jpgstoreapis.com/search/tokens?policyIds=[%22{puurrtybot.POLICY}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size=300""").json()['tokens']
        for listing in listings:
            if ddq.get_listing_by_id(f"""{listing['listed_at']}_{listing['asset_name']}"""):
                break;
            else:
                untracked_listings[f"""{listing['listed_at']}_{listing['asset_name']}"""] = listing

        for listing_id, listing in list(untracked_listings.items())[::-1]:
            timestamp = pf.time_to_timestamp(listing['created_at'].split('.')[0].split('+')[0].replace('T',' '))
            amount = int(listing['listing_lovelace'])/1_000_000
            untracked_listings[listing_id] = {'listing_id': listing_id, 'timestamp':timestamp, 'asset': listing['asset_name'], 'amount':amount, 'market':'jpgstore'}
            #ddi.listing_new(listing_id = listing_id, asset_id = listing['asset_name'], timestamp = timestamp, amount = int(listing['listing_lovelace']))
    #return untracked_listings
      