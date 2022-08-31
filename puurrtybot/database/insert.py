from puurrtybot.database.create import Address, User, Sale, Listing, Tweet, sql_insert
from puurrtybot.database.table import Table
import puurrtybot.database.query as dq
import puurrtybot.api.blockfrostio as blockfrostio


@sql_insert
def insert_row(row: Table) -> None:
    if dq.fetch_row(row) is None:
        return row.__class__(**row.dictionary)


def new_user(user_id, username):
    insert_row(User(user_id = user_id, username = username))


def new_address_stake_address(address, stake_address, user_id):
    insert_row(Address(address = address, stake_address = stake_address, user_id = user_id))


def new_address(address, user_id):
    stake_address = blockfrostio.get_stake_address_by_address(address)
    insert_row(Address(address = address, stake_address = stake_address, user_id = user_id))


def new_sale(tx_hash, asset_id, timestamp, amount, tracked = True):
    insert_row(Sale(tx_hash = tx_hash, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))


def new_listing(listing_id, asset_id, timestamp, amount, tracked = True):
    insert_row(Listing(listing_id = listing_id, asset_id = asset_id, created_at = timestamp, amount = amount, tracked = tracked))


def new_tweet(tweet_id, author_id, in_reply_to_user_id = None, tracked = True):
    insert_row(Tweet(tweet_id = tweet_id, author_id = author_id, in_reply_to_user_id = in_reply_to_user_id, tracked = tracked))