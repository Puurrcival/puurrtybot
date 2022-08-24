import datetime
from typing import List

import requests
from requests.models import Response

from puurrtybot.database.create import Sale, Listing
from puurrtybot.pcs import POLICY_ID
import puurrtybot.databases.database_queries as ddq

NETWORK = """https://server.jpgstoreapis.com"""
JPGSTORE_STATUS_CODES = {
    #
    400: """The request is not valid."""}


def query(query_string: str) -> Response:
    """Query blockfrost.io and check for valid response."""
    response = requests.get(f"""{NETWORK}{query_string}""")
    if response.status_code != 200:
        raise Exception( (response.status_code, JPGSTORE_STATUS_CODES[response.status_code]) )
    return response


def time_to_timestamp(timeformat):
    timeformat = timeformat.split('.')[0].split('+')[0].replace('T',' ')
    return int(datetime.datetime.strptime(timeformat,"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def get_sale_last():
    return query(f"""{NETWORK}/collection/{POLICY_ID}/transactions?page=1&count=1""").json()['transactions'][0]


def get_sales(count: int):
    response = query(f"""/collection/{POLICY_ID}/transactions?page=1&count={count}""")
    return [Sale(   tx_hash = sale['tx_hash'],
                    asset_id = sale['asset_id'],
                    action = sale['action'],
                    created_at = time_to_timestamp(sale['created_at']),
                    confirmed_at = time_to_timestamp(sale.get('confirmed_at')) if sale.get('confirmed_at') else None,
                    buyer_address = sale['signer_address'],
                    seller_address = sale['seller_address'],
                    amount_lovelace = int(sale['amount_lovelace']),
                    market = "jpgstore",
                    tracked = True
                    ) for sale in response.json()['transactions']]


def get_sales_untracked() -> List[Sale]:
    untracked_sales = []
    last_sale = get_sale_last()
    if not ddq.get_sale_by_tx_hash(last_sale['tx_hash']):
        count = 50
        while count:
            sales = get_sales(count)
            count+=50
            for sale in sales:
                if ddq.get_sale_by_tx_hash(sale.tx_hash):
                    count = None
                    break;
                else:
                    untracked_sales.append(sale)
    return list(set(untracked_sales))


def get_listings(count: int):
    response = query(f"""/search/tokens?policyIds=[%22{POLICY_ID}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size={count}""")
    return [Listing(f"""{listing['asset_id']}_{time_to_timestamp(listing['created_at'])}""",
                    listing['asset_id'],
                    time_to_timestamp(listing['created_at']),
                    int(listing['listing_lovelace']),
                    "jpgstore",
                    True
                    ) for listing in response.json()['tokens']]