from typing import List, Union

from sqlalchemy import or_, and_

from puurrtybot.database.create import Listing, User, Address, Asset, Role, Sale, Tweet, sql_query
from puurrtybot.pcs.metadata import Trait
from puurrtybot.pcs.role import AssetRole, Amount


"""User queries."""
@sql_query
def get_user_all(session=None) -> List[User]:
    """Get all user data."""
    return session.query(User).all()
    

@sql_query
def get_user_by_user_id(user_id: int, session=None) -> User:
    """Get user data by user_id."""
    return session.query(User).filter(User.user_id == user_id).first()
#print(get_user_by_user_id(user_id = 642352900357750787))

@sql_query
def get_user_by_twitter_id(twitter_id: int, session=None) -> User:
    """Get user data by twitter_id."""
    return session.query(User).filter(User.twitter_id == twitter_id).first()


@sql_query
def get_user_by_asset_id(asset_id: str, session=None) -> User:
    """Get user data by asset_id."""
    return session.query(User).filter(Asset.asset_id == asset_id).filter(Asset.address == Address.address).filter(Address.user_id == User.user_id).first()


"""Address queries"""
@sql_query
def get_address_by_address(address: str, session=None) -> Address:
    """Get address data by address."""
    return session.query(Address).filter(Address.address == address).first()


@sql_query
def get_address_by_user_id(user_id: int, session=None) -> List[Address]:
    return session.query(Address).filter(Address.user_id == user_id)


"""Asset queries."""
@sql_query
def get_asset_by_asset_id(asset_id: str, session=None) -> Asset:
    """Get asset data by asset_id."""
    return session.query(Asset).filter(Asset.asset_id == asset_id).first()


@sql_query
def get_asset_all(timestamp: int = None, session=None) -> List[Asset]:
    """Get data of all assets before a timestamp."""
    return session.query(Asset).filter(Asset.updated_on < timestamp).all() if timestamp else session.query(Asset).all()


@sql_query
def get_asset_all_by_user_id(user_id: int, count: bool = True, session=None) -> Union[int, List[Asset]]:
    """Get count or data of all assetes of an user by user_id."""
    session = session.query(Asset).filter(User.user_id == Address.user_id).filter(Address.address == Asset.address).filter(User.user_id == user_id)
    return session.count() if count else session.all()


@sql_query
def get_asset_all_by_role(role: AssetRole, user_id: int = None, count: bool = True, session=None) -> Union[int, List[Asset]]:
    """Get count or data of all assetes matching a role, optional of an user by user_id."""
    session = session.query(Asset).filter(or_(getattr(Asset, trait.class_name)==trait for trait in role.requirement))
    if user_id:
        session = session.filter(
                    User.user_id == Address.user_id).filter(
                    Address.address == Asset.address).filter(
                    User.user_id == user_id)
    return session.count() if count else session.all()


"""Tweet queries."""
@sql_query
def get_tweet_by_tweet_id(tweet_id: int, session=None) -> Tweet:
    """Get tweet data by tweet_id."""
    return session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()


"""Sale queries"""
@sql_query
def get_sale_by_tx_hash(tx_hash: str, session=None) -> Sale:
    """Get sale data by tx_hash."""
    return session.query(Sale).filter(Sale.tx_hash == tx_hash).first()


@sql_query
def get_sale_history(asset_id: str, session=None) -> List[Sale]:
    """Get sale data of an asset by asset_id."""
    sales = session.query(Sale).filter(Sale.asset_id == asset_id).filter(Sale.tracked == True).all()
    sales.sort(key=lambda x: x.confirmed_at, reverse=False)
    return sales


"""Listing queries."""
@sql_query
def get_listing_by_id(listing_id, session=None) -> Sale:
    """Get data of listing by listing_id."""
    return session.query(Listing).filter(Listing.listing_id == listing_id).first()


@sql_query
def get_listings(tracked: bool = True, session=None) -> List[Listing]:
    """Get data of all listings, latest first."""
    listings = session.query(Listing).filter(Listing.tracked == tracked).all()
    listings.sort(key=lambda x: x.created_at, reverse=False)
    return listings

 
"""Role queries."""
def qualify_role(role_object: AssetRole, user_id: int) -> int:
    """Check if a user meets the requirements for a role."""
    if type(role_object) is Amount:
        amount = get_asset_all_by_user_id(user_id)
        if amount >= min(role_object.requirement) and amount <= max(role_object.requirement):
            return amount
    else:
        result = get_asset_all_by_role(role_object, user_id)
        if result > 0:
            return result
    return 0


@sql_query
def get_role_all(session=None) -> List[Role]:
    """Get all role data."""
    return session.query(Role).all()


@sql_query
def get_role_by_user_id(user_id: int, session=None) -> List[Role]:
    """Get all role data."""
    return session.query(Role).filter(Role.user_id == user_id).all()


@sql_query
def get_amount_of_assets_for_role(role_id: int, user_id: int, session=None) -> bool:
    """Get amount of assets that qualify for a role."""
    return session.query(Role).filter(and_(Role.role_id == role_id, Role.user_id == user_id, Role.requirement)).first().requirement


"""Query Traits."""
@sql_query
def get_amount_of_assets_for_trait(trait_list: List[Trait], user_id: int, session=None) -> int:
    return session.query(Asset).filter(
        or_(getattr(Asset, trait.class_name) == trait for trait in trait_list)).filter(
        User.user_id == Address.user_id).filter(
        Address.address == Asset.address).filter(
        User.user_id == user_id).count()