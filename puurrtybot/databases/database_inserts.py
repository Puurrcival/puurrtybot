from puurrtybot.database.create import Address, Asset, User, Sale, Listing, Tweet, Session
import puurrtybot.databases.database_queries as ddq
import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.functions as func


def user_change_balance(user_id, amount):
    Session.query(User).filter(User.user_id == user_id).update({'balance': User.balance + amount})
    Session.commit()


def asset_change_address(asset_id, address):
    address_type = blockfrost.get_address_type(address)
    stake_address = blockfrost.get_stake_address_by_address(address)
    stake_address_type = blockfrost.get_address_type(stake_address)
    Session.query(Asset).filter(Asset.asset_id == asset_id).update(
        {'address': address,
         'address_type': address_type.name if address_type else None,
         'stake_address': stake_address,
         'stake_address_type': stake_address_type.name if stake_address_type else None,
         'updated_on':func.get_utc_time()})
    Session.commit()


def user_change_twitter(user_id, twitter_id, twitter_handle):
    Session.query(User).filter(User.user_id == user_id).update({'twitter_id': twitter_id, 'twitter_handle': twitter_handle})
    Session.commit()


def user_new(user_id, username):
    if ddq.get_user_by_id(user_id) is None:
        Session.add(User(user_id = user_id, username = username))
        Session.commit()


def address_stake_address_new(address, stake_address, user_id):
    Session.add(Address(address = address, stake_address = stake_address, user_id = user_id))
    Session.commit()


def address_new(address, user_id):
    stake_address = blockfrost.get_stake_address_by_address(address)
    Session.add(Address(address = address, stake_address = stake_address, user_id = user_id))
    Session.commit()


def sale_new(tx_hash, asset_id, timestamp, amount, tracked = False):
    Session.add(Sale(tx_hash = tx_hash, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    Session.commit()


def sale_tracked(tx_hash):
    Session.query(Sale).filter(Sale.tx_hash == tx_hash).update({'tracked': True})
    Session.commit()


def listing_new(listing_id, asset_id, timestamp, amount, tracked = False):
    Session.add(Listing(listing_id = listing_id, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    Session.commit()


def listing_tracked(listing_id):
    Session.query(Listing).filter(Listing.listing_id == listing_id).update({'tracked': True})
    Session.commit()


def tweet_new(tweet_id, author_id, in_reply_to_user_id = None, tracked = False):
    Session.add(Tweet(tweet_id = tweet_id, author_id = author_id, in_reply_to_user_id = in_reply_to_user_id, tracked = tracked))
    Session.commit()


def tweet_tracked(tweet_id):
    Session.query(Tweet).filter(Tweet.tweet_id == tweet_id).update({'tracked': True})
    Session.commit()