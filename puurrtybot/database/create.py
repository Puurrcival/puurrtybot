"""A module to create the sqlite .db"""
from datetime import datetime

from pycardano import AddressType
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, create_engine, Enum
from sqlalchemy.orm import relationship, sessionmaker, registry

from puurrtybot.pcs import metadata
from puurrtybot.database import address, listing, sale, tweet, user
from puurrtybot.pcs import asset, role
from puurrtybot import DATABASES_DIR


mapper_registry = registry()

Base = mapper_registry.generate_base()

engine = create_engine(f"""sqlite:///{DATABASES_DIR}/pcs.db""")

Session = sessionmaker()
         

@mapper_registry.mapped
class Sale(sale.Sale):
    __table__ = Table(
        "sales",
        mapper_registry.metadata,
        Column('tx_hash', String(255), primary_key=True),
        Column('asset_id', String(255), ForeignKey('assets.asset_id')),
        Column('action', String(255)),
        Column('created_at', Integer()),
        Column('confirmed_at', Integer()),
        Column('buyer_address', String(255)),
        Column('seller_address', String(255)),
        Column('amount_lovelace', Integer()),
        Column('market', String(255)),
        Column('tracked', Boolean(), default=False),
    )


@mapper_registry.mapped
class Asset(asset.Asset):
    __table__ = Table(
        "assets",
        mapper_registry.metadata,
        Column('asset_id', String(127), primary_key=True),
        Column('address', String(255), ForeignKey('addresses.address')),
        Column('address_type', Enum(AddressType)),
        Column('stake_address', String(255)),
        Column('stake_address_type', Enum(AddressType)),
        Column('policy_id', String(255)),
        Column('asset_fingerprint', String(63)),
        Column('initial_mint_tx_hash', String(63)),
        Column('quantity', Integer()),
        Column('asset_name', String(63)),          
        Column('name', String(63)),
        Column('prefix_name', Enum(metadata.Prefix_name)),
        Column('first_name', Enum(metadata.First_name)),
        Column('last_name', Enum(metadata.Last_name)),
        Column('suffix_name', Enum(metadata.Suffix_name)),
        Column('img_url', String(255)),
        Column('unique', Enum(metadata.Unique)),                      
        Column('fur', Enum(metadata.Fur)), 
        Column('hat', Enum(metadata.Hat)), 
        Column('eyes', Enum(metadata.Eyes)), 
        Column('mask', Enum(metadata.Mask)), 
        Column('tail', Enum(metadata.Tail)), 
        Column('hands', Enum(metadata.Hands)), 
        Column('mouth', Enum(metadata.Mouth)), 
        Column('wings', Enum(metadata.Wings)), 
        Column('outfit', Enum(metadata.Outfit)), 
        Column('background', Enum(metadata.Background)),
        Column('collection', String(31)), 
        Column('mint_price', Integer()),
        Column('mint_time', Integer()),
        Column('updated_on', Integer(), default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()))
    )

    __mapper_args__ = {
        "properties": {
            "sales": relationship("Sale"),
        }
    }


@mapper_registry.mapped
class Address(address.Address):
    __table__ = Table(
        "addresses",
        mapper_registry.metadata,
        Column('address', String(255), primary_key=True),
        Column('stake_address', String(255)),
        Column('user_id', ForeignKey('users.user_id'))
    )
        
    __mapper_args__ = {
        "properties": {
            "assets": relationship("Asset"),
        }
    }
    

@mapper_registry.mapped
class Listing(listing.Listing):
    __table__ = Table(
        "listings",
        mapper_registry.metadata,
        Column('listing_id', String(255), primary_key=True),
        Column('asset_id', String(255), ForeignKey('assets.asset_id')),
        Column('created_at', Integer()),
        Column('amount_lovelace', Integer()),
        Column('market', String(255)),
        Column('tracked', Boolean(), default=False),
    )


@mapper_registry.mapped
class Tweet(tweet.Tweet):
    __table__ = Table(
        "tweets",
        mapper_registry.metadata,
        Column('tweet_id', Integer(), primary_key=True),
        Column('created_at', Integer()),
        Column('author_id', Integer(), ForeignKey('users.twitter_id')),
        Column('in_reply_to_user_id', Integer()),
        Column('tracked', Boolean(), default=False),
    )


@mapper_registry.mapped
class Role(role.Role):
    __table__ = Table(
        "roles",
        mapper_registry.metadata,
        Column('ix', String(255), primary_key=True),
        Column('role_id', Integer()),
        Column('user_id', String(255), ForeignKey('users.user_id')),
        Column('requirement', Boolean(), default=False),
        Column('updated_on', Integer(), default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()))
    )


@mapper_registry.mapped
class User(user.User):
    __table__ = Table(
        "users",
        mapper_registry.metadata,
        Column('user_id', Integer(), primary_key=True),
        Column('balance', Integer(), default=0),
        Column('username', String(31)),
        Column('twitter_id', Integer()),
        Column('twitter_handle', String(255)),
        Column('updated_on', Integer(), default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()))
    )

    __mapper_args__ = {
        "properties": {
            "addresses": relationship("Address"),
            "roles": relationship("Role"),
            "tweets": relationship("Tweet"),
        }
    }

Base.metadata.create_all(engine)


session = Session(bind=engine)


def sql_add(sql_function):
    def wrapper(*args, **kwargs):
        with Session(bind=engine) as session:
            result = sql_function(*args, **kwargs)
            if type(result) is list:
                session.add_all(result)
            else:
                session.add(result)
            session.commit()
    return wrapper


def sql_query(sql_function):
    def wrapper(*args, **kwargs):
        with Session(bind=engine) as session:
            kwargs['session'] = session
            return sql_function(*args, **kwargs)
    return wrapper


def sql_update(sql_function):
    def wrapper(*args, **kwargs):
        with Session(bind=engine) as session:
            kwargs['session'] = session
            sql_function(*args, **kwargs)
            kwargs['session'].commit()
    return wrapper