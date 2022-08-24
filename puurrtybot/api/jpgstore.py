import datetime
from typing import List

import requests
from requests.models import Response

from puurrtybot.database.create import Sale, Listing
import puurrtybot.databases.database_queries as ddq

NETWORK = """https://server.jpgstoreapis.com"""
JPGSTORE_STATUS_CODES = {
    #
    400: """The request is not valid."""}


def query(query_string: str) -> Response:
    """Query jpg.store and check for valid response."""
    response = requests.get(f"""{NETWORK}{query_string}""")
    if response.status_code != 200:
        raise Exception( (response.status_code, JPGSTORE_STATUS_CODES[response.status_code]) )
    return response


def time_to_timestamp(timeformat):
    timeformat = timeformat.split('.')[0].split('+')[0].replace('T',' ')
    return int(datetime.datetime.strptime(timeformat,"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def map_sale(sale: dict):
    return Sale(    tx_hash = sale['tx_hash'],
                    asset_id = sale['asset_id'],
                    action = sale['action'],
                    created_at = time_to_timestamp(sale['created_at']),
                    confirmed_at = time_to_timestamp(sale.get('confirmed_at')) if sale.get('confirmed_at') else None,
                    buyer_address = sale['signer_address'],
                    seller_address = sale['seller_address'],
                    amount_lovelace = int(sale['amount_lovelace']),
                    market = "jpgstore",
                    tracked = True
                    )


def map_listing(listing: dict):
    return Listing( listing_id = f"""{listing['asset_id']}_{time_to_timestamp(listing['created_at'])}""",
                    asset_id = listing['asset_id'],
                    created_at = time_to_timestamp(listing['created_at']),
                    amount_lovelace = int(listing['listing_lovelace']),
                    market = "jpgstore",
                    tracked = True
                    )


def get_sale_last(policy_id: str) -> Sale:
    return map_sale(query(f"""/collection/{policy_id}/transactions?page=1&count=1""").json()['transactions'][0])


def get_sales(policy_id: str, count: int) -> List[Sale]:
    response = query(f"""/collection/{policy_id}/transactions?page=1&count={count}""")
    return [map_sale(sale) for sale in response.json()['transactions']]


def get_sales_untracked(policy_id: str) -> List[Sale]:
    untracked_sales = {}
    count = 50
    while count:
        sales = get_sales(policy_id, count)
        count+=50
        for sale in sales:
            if ddq.get_sale_by_tx_hash(sale.tx_hash):
                count = None
                break
            else:
                untracked_sales[sale.tx_hash] = sale
    return list(untracked_sales.values())


def get_listing_last(policy_id: str) -> Listing:
    response = query(f"""/search/tokens?policyIds=[%22{policy_id}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size=1""")
    return map_listing(response.json()['tokens'][0])


def get_listings(policy_id: str, count: int) -> List[Listing]:
    response = query(f"""/search/tokens?policyIds=[%22{policy_id}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size={count}""")
    return [map_listing(listing) for listing in response.json()['tokens']]


def get_listings_untracked(policy_id: str) -> List[Listing]:
    untracked_listings = {}
    count = 50
    while count:
        listings = get_listings(policy_id, count)
        count+=50
        for listing in listings:
            if ddq.get_listing_by_id(listing.listing_id):
                count = None
                break
            else:
                untracked_listings[listing.listing_id] = listing
    return list(untracked_listings.values())