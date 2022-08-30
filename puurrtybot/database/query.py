from typing import List, Union, Type

from sqlalchemy import or_, and_
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from puurrtybot.database.create import Listing, User, Address, Asset, Role, Sale, Tweet, sql_query
from puurrtybot.database.table import Table
from puurrtybot.pcs.metadata import Trait
from puurrtybot.pcs.role import AssetRole, Amount, Family


"""Universal queries."""
@sql_query
def fetch_row_by_value(row: Table, column: Union[str, InstrumentedAttribute], value, all = False, detach: bool = True, session: Session = None) -> List[Table]:
    """Fetch a row by a value in a column."""
    table = row if isinstance(row.table, property) else row.table
    column = column if type(column) is InstrumentedAttribute else getattr(table, column)
    session = session.query(table).filter(column == value)
    return session.all() if all else session.first()

#print(fetch_row_by_value(Address, Address.user_id, value=642352900357750787, all=True))


def fetch_row(row: Table) -> Table:
    """Fetch a row by primary key."""
    return fetch_row_by_value(row, row.primary_key, getattr(row, row.primary_key))


#print(fetch_row(Sale(tx_hash='28e279c1b615dea082f4fdc9c430c325a239bca004152b39116bb6bd1993de3c')))


@sql_query
def fetch_table(table: Type[Table], detach: bool = True, session: Session = None) -> List[Table]:
    """Fetch all rows of a table."""
    return session.query(table).all()


"""User queries."""
@sql_query
def get_user_by_asset_id(asset_id: str, detach: bool = True, session: Session = None) -> User:
    """Get user data by asset_id."""
    return session.query(User).filter(Asset.asset_id == asset_id).filter(Asset.address == Address.address).filter(Address.user_id == User.user_id).first()


"""Asset queries."""
@sql_query
def get_asset_by_asset_id(asset_id: str, detach: bool = True, session: Session = None) -> Asset:
    """Get asset data by asset_id."""
    return session.query(Asset).filter(Asset.asset_id == asset_id).first()


@sql_query
def get_asset_all(timestamp: int = None, detach: bool = True, session: Session = None) -> List[Asset]:
    """Get data of all assets before a timestamp."""
    return session.query(Asset).filter(Asset.updated_on < timestamp).all() if timestamp else session.query(Asset).all()


@sql_query
def get_asset_all_by_user_id(user_id: int, count: bool = True, detach: bool = True, session: Session = None) -> Union[int, List[Asset]]:
    """Get count or data of all assetes of an user by user_id."""
    session = session.query(Asset).filter(User.user_id == Address.user_id).filter(Address.address == Asset.address).filter(User.user_id == user_id)
    return session.count() if count else session.all()


@sql_query
def get_asset_all_by_role(role: AssetRole, user_id: int = None, count: bool = True, detach: bool = True, session: Session = None) -> Union[int, List[Asset]]:
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
def get_tweet_by_tweet_id(tweet_id: int, detach: bool = True, session: Session = None) -> Tweet:
    """Get tweet data by tweet_id."""
    return session.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()


"""Sale queries"""
@sql_query
def get_sale_history(asset_id: str, detach: bool = True, session: Session = None) -> List[Sale]:
    """Get sale data of an asset by asset_id."""
    sales = session.query(Sale).filter(Sale.asset_id == asset_id).filter(Sale.tracked == True).all()
    sales.sort(key=lambda x: x.confirmed_at, reverse=False)
    return sales


"""Listing queries."""
@sql_query
def get_listings(tracked: bool = True, detach: bool = True, session: Session = None) -> List[Listing]:
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
def get_role_by_user_id(user_id: int, detach: bool = True, session: Session = None) -> List[Role]:
    """Get all role data."""
    return session.query(Role).filter(Role.user_id == user_id).all()


@sql_query
def check_role_requirement(role_id: int, user_id: int, detach: bool = True, session: Session = None) -> bool:
    """Get amount of assets that qualify for a role."""
    return True if session.query(Role).filter(and_(Role.role_id == role_id, Role.user_id == user_id, Role.requirement)).first() else False


"""Query Traits."""
@sql_query
def get_amount_of_assets_for_trait(trait_list: List[Trait], user_id: int, detach: bool = True, session: Session = None) -> int:
    return session.query(Asset).filter(
        or_(getattr(Asset, trait.class_name) == trait for trait in trait_list)).filter(
        User.user_id == Address.user_id).filter(
        Address.address == Asset.address).filter(
        User.user_id == user_id).count()