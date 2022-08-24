from sqlalchemy import or_

from puurrtybot.database.create import Listing, SESSION, User, Address, Asset, Sale, Tweet
from puurrtybot.pcs import role

def get_user_by_id(user_id):
    return SESSION.query(User).filter(User.user_id == user_id).first()


def get_address_by_address(address):
    return SESSION.query(Address).filter(Address.address == address).first()


def get_user_by_twitter_id(twitter_id):
    return SESSION.query(User).filter(User.twitter_id == twitter_id).first()


def get_asset_by_id(asset_id):
    return SESSION.query(Asset).filter(Asset.asset_id == asset_id).first()


def get_all_assets():
    return SESSION.query(Asset).all()


def get_asset_all(timestamp = 999_999_999_999):
    return SESSION.query(Asset).filter(Asset.updated_on < timestamp).all()


def get_tweet_by_id(tweet_id):
    return SESSION.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()


def get_user_number_of_assets(user_id):
    return SESSION.query(Asset).filter(User.user_id == Address.user_id).filter(Address.address == Asset.address).filter(User.user_id == user_id).count()


def get_address_by_address(address):
    return SESSION.query(Address).filter(Address.address == address).first()


def get_sale_by_tx_hash(tx_hash):
    return SESSION.query(Sale).filter(Sale.tx_hash == tx_hash).first()


def get_sales(tracked = False):
    sales = SESSION.query(Sale).filter(Sale.tracked == tracked).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_listings(tracked = False):
    listings = SESSION.query(Listing).filter(Listing.tracked == tracked).all()
    listings.sort(key=lambda x: x.timestamp, reverse=False)
    return listings


def get_tweets(tracked = False):
    tweets = SESSION.query(Tweet).filter(Tweet.tracked == tracked).all()
    #listings.sort(key=lambda x: x.timestamp, reverse=False)
    return tweets


def get_sales_history(asset_id):
    sales = SESSION.query(Sale).filter(Sale.asset_id == asset_id).filter(Sale.tracked == True).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_listing_by_id(listing_id):
    return SESSION.query(Listing).filter(Listing.listing_id == listing_id).first()


### Roles ###
def check_role_qualify(role_object: role.Role, user_id: int) -> int:
    requirement = role_object.value.requirement
    session = SESSION.query(Asset
                        ).filter(User.user_id == Address.user_id
                        ).filter(Address.address == Asset.address
                        ).filter(User.user_id == user_id
                        )

    if type(role_object) is role.Amount:
        amount = len(session.all())
        if amount >= min(requirement) and amount <= max(requirement):
            return amount
    else:
        result = session.filter(or_(getattr(Asset, trait.class_name())==trait for trait in requirement)
                        ).all()
        if len(result) > 0:
            return len(result)
    return 0