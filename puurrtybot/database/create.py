"""A module to create the sqlite .db"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, sessionmaker, registry

from puurrtybot.database import address, asset, listing, sale, tweet, user
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
        Column('address_type', String(63)),
        Column('stake_address', String(255)),
        Column('stake_address_type', String(63)),
        Column('policy_id', String(255)),
        Column('asset_fingerprint', String(63)),
        Column('initial_mint_tx_hash', String(63)),
        Column('quantity', Integer()),
        Column('asset_name', String(63)),          
        Column('name', String(63)),
        Column('prefix_name', String(63)),
        Column('first_name', String(63)),
        Column('last_name', String(63)),
        Column('suffix_name', String(63)),
        Column('img_url', String(63)),
        Column('unique', String(31)),                      
        Column('fur', String(31)), 
        Column('hat', String(31)), 
        Column('eyes', String(31)), 
        Column('mask', String(31)), 
        Column('tail', String(31)), 
        Column('hands', String(31)), 
        Column('mouth', String(31)), 
        Column('wings', String(31)), 
        Column('outfit', String(31)), 
        Column('background', String(31)), 
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
        }
    }
    

@mapper_registry.mapped
class Listing(listing.Listing):
    __table__ = Table(
        "listings",
        mapper_registry.metadata,
        Column('listing_id', String(255), primary_key=True),
        Column('asset_id', String(255), ForeignKey('assets.asset_id')),
        Column('listed_at', Integer()),
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
        Column('author_id', Integer()),
        Column('in_reply_to_user_id', Integer()),
        Column('tracked', Boolean(), default=False),
    )


Base.metadata.create_all(engine)
Session = Session(bind=engine)