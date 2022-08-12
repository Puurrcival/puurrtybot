from puurrtybot.databases.database_initialize import Address, Asset, User, Sale, Listing, Session
import puurrtybot.databases.database_queries as ddq
import puurrtybot.blockfrost.blockfrost_queries as bbq


def user_change_balance(user_id, amount):
    Session.query(User).filter(User.user_id == user_id).update({'balance': User.balance + amount})
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
    stake_address = bbq.get_stake_address_by_address(address)
    Session.add(Address(address = address, stake_address = stake_address, user_id = user_id))
    Session.commit()


def sale_new(tx_hash, asset_id, timestamp, amount, tracked = False):
    Session.add(Sale(tx_hash = tx_hash, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    Session.commit()


def sale_tracked(tx_hash):
    Session.query(Sale).filter(Sale.tx_hash == tx_hash).update({'tracked': True})
    Session.commit()


def listing_new(listing_id, asset_id, timestamp, amount, tracked = True):
    Session.add(Listing(listing_id = listing_id, asset_id = asset_id, timestamp = timestamp, amount = amount, tracked = tracked))
    Session.commit()