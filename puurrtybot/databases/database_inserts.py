from puurrtybot.database.create import Address, Asset, User, Sale, Listing, Tweet, SESSION
import puurrtybot.databases.database_queries as ddq
import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.functions as func


def user_change_balance(user_id, amount):
    SESSION.query(User).filter(User.user_id == user_id).update({'balance': User.balance + amount})
    SESSION.commit()


def asset_change_address(asset_id, address):
    address_type = blockfrost.get_address_type(address)
    stake_address = blockfrost.get_stake_address_by_address(address)
    stake_address_type = blockfrost.get_address_type(stake_address)
    SESSION.query(Asset).filter(Asset.asset_id == asset_id).update(
        {'address': address,
         'address_type': address_type.name if address_type else None,
         'stake_address': stake_address,
         'stake_address_type': stake_address_type.name if stake_address_type else None,
         'updated_on':func.get_utc_time()})
    SESSION.commit()


def user_change_twitter(user_id, twitter_id, twitter_handle):
    SESSION.query(User).filter(User.user_id == user_id).update({'twitter_id': twitter_id, 'twitter_handle': twitter_handle})
    SESSION.commit()


def user_new(user_id, username):
    if ddq.get_user_by_id(user_id) is None:
        SESSION.add(User(user_id = user_id, username = username))
        SESSION.commit()


def address_stake_address_new(address, stake_address, user_id):
    SESSION.add(Address(address = address, stake_address = stake_address, user_id = user_id))
    SESSION.commit()


def address_new(address, user_id):
    stake_address = blockfrost.get_stake_address_by_address(address)
    SESSION.add(Address(address = address, stake_address = stake_address, user_id = user_id))
    SESSION.commit()


def sale_new(tx_hash, asset_id, timestamp, amount, tracked = False):
    SESSION.add(Sale(tx_hash = tx_hash, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    SESSION.commit()


def sale_tracked(tx_hash):
    SESSION.query(Sale).filter(Sale.tx_hash == tx_hash).update({'tracked': True})
    SESSION.commit()


def listing_new(listing_id, asset_id, timestamp, amount, tracked = False):
    SESSION.add(Listing(listing_id = listing_id, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    SESSION.commit()


def listing_tracked(listing_id):
    SESSION.query(Listing).filter(Listing.listing_id == listing_id).update({'tracked': True})
    SESSION.commit()


def tweet_new(tweet_id, author_id, in_reply_to_user_id = None, tracked = False):
    SESSION.add(Tweet(tweet_id = tweet_id, author_id = author_id, in_reply_to_user_id = in_reply_to_user_id, tracked = tracked))
    SESSION.commit()


def tweet_tracked(tweet_id):
    SESSION.query(Tweet).filter(Tweet.tweet_id == tweet_id).update({'tracked': True})
    SESSION.commit()