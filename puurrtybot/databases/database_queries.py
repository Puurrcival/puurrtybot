from puurrtybot.databases.database_initialize import Listing, Session, User, Address, Asset, Sale, Tweet
from sqlalchemy import or_
import puurrtybot

def get_user_by_id(user_id):
    return Session.query(User).filter(User.user_id == user_id).first()


def get_user_by_twitter_id(twitter_id):
    return Session.query(User).filter(User.twitter_id == twitter_id).first()


def get_asset_by_id(asset_id):
    return Session.query(Asset).filter(Asset.asset_id == asset_id).first()


def get_asset_all(timestamp = 999_999_999):
    return Session.query(Asset).filter(Asset.updated_on < timestamp).all()


def get_tweet_by_id(tweet_id):
    return Session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()


def get_user_number_of_assets(user_id):
    return Session.query(Asset).filter(User.user_id == Address.user_id).filter(Address.address == Asset.address).filter(User.user_id == user_id).count()


def get_address_by_address(address):
    return Session.query(Address).filter(Address.address == address).first()


def get_sale_by_tx_hash(tx_hash):
    return Session.query(Sale).filter(Sale.tx_hash == tx_hash).first()


def get_sales(tracked = False):
    sales = Session.query(Sale).filter(Sale.tracked == tracked).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_listings(tracked = False):
    listings = Session.query(Listing).filter(Listing.tracked == tracked).all()
    listings.sort(key=lambda x: x.timestamp, reverse=False)
    return listings


def get_tweets(tracked = False):
    tweets = Session.query(Tweet).filter(Tweet.tracked == tracked).all()
    #listings.sort(key=lambda x: x.timestamp, reverse=False)
    return tweets


def get_sales_history(asset_id):
    sales = Session.query(Sale).filter(Sale.asset_id == asset_id).filter(Sale.tracked == True).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_listing_by_id(listing_id):
    return Session.query(Listing).filter(Listing.listing_id == listing_id).first()


### Roles ###
def get_trait_role_qualify(role_id, user_id):
    try:
        traits = puurrtybot.ROLES_BASED_ON_FAMILY[role_id]
    except KeyError:
        traits = puurrtybot.ROLES_BASED_ON_TRAITS[role_id]
    result = Session.query(Asset
                    ).filter(User.user_id == Address.user_id
                    ).filter(Address.address == Asset.address
                    ).filter(User.user_id == user_id
                    ).filter( or_(getattr(Asset, k)==v for k,v in traits)
                    ).all()
    return len(result)


def get_traits_role_qualify(traits, user_id):
    result = Session.query(Asset
                    ).filter(User.user_id == Address.user_id
                    ).filter(Address.address == Asset.address
                    ).filter(User.user_id == user_id
                    ).filter( or_(getattr(Asset, k)==v for k,v in traits)
                    ).all()
    return len(result)