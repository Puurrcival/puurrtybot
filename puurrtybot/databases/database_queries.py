from puurrtybot.databases.database_initialize import Listing, Session, User, Address, Asset, Sale
from sqlalchemy import or_
import puurrtybot

def get_user_by_id(user_id):
    return Session.query(User).filter(User.user_id == user_id).first()


def get_asset_by_id(asset_id):
    return Session.query(Asset).filter(Asset.asset_id == asset_id).first()


def get_user_number_of_assets(user_id):
    return Session.query(Asset).filter(User.user_id == Address.user_id).filter(Address.address == Asset.address).filter(User.user_id == user_id).count()


def get_address_by_address(address):
    return Session.query(Address).filter(Address.address == address)


def get_sale_by_tx_hash(tx_hash):
    return Session.query(Sale).filter(Sale.tx_hash == tx_hash).first()


def get_sales(tracked = False):
    sales = Session.query(Sale).filter(Sale.tracked == tracked).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_sales_history(asset_id):
    sales = Session.query(Sale).filter(Sale.asset_id == asset_id).filter(Sale.tracked == True).all()
    sales.sort(key=lambda x: x.timestamp, reverse=False)
    return sales


def get_listing_by_id(listing_id):
    return Session.query(Listing).filter(Listing.listing_id == listing_id).first()


### Roles ###
def get_trait_role_qualify(role_id, user_id):
    traits = puurrtybot.ROLES_BASED_ON_TRAITS[role_id]
    result = Session.query(Asset
                    ).filter(User.user_id == Address.user_id
                    ).filter(Address.address == Asset.address
                    ).filter(User.user_id == user_id
                    ).filter( or_(getattr(Asset, k)==v for k,v in traits)
                    ).all()
    return len(result)