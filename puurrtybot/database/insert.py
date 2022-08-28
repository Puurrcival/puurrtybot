from puurrtybot.database.create import Address, User, Sale, Listing, Tweet, sql_insert
import puurrtybot.database.query as dq
import puurrtybot.api.blockfrost as blockfrost


@sql_insert
def insert_object(sql_object) -> None:
    return sql_object.__class__(**sql_object.dictionary)


def new_user(user_id, username):
    if dq.get_user_by_user_id(user_id) is None:
        insert_object(User(user_id = user_id, username = username))


def new_address_stake_address(address, stake_address, user_id):
    insert_object(Address(address = address, stake_address = stake_address, user_id = user_id))


def new_address(address, user_id):
    stake_address = blockfrost.get_stake_address_by_address(address)
    insert_object(Address(address = address, stake_address = stake_address, user_id = user_id))


def new_sale(tx_hash, asset_id, timestamp, amount, tracked = True):
    insert_object(Sale(tx_hash = tx_hash, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))


def new_listing(listing_id, asset_id, timestamp, amount, tracked = True):
    insert_object(Listing(listing_id = listing_id, asset_id = asset_id, created_at = timestamp, amount = amount, tracked = tracked))


def new_tweet(tweet_id, author_id, in_reply_to_user_id = None, tracked = True):
    insert_object(Tweet(tweet_id = tweet_id, author_id = author_id, in_reply_to_user_id = in_reply_to_user_id, tracked = tracked))