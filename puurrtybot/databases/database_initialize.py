import puurrtybot
from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, registry
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional
import tqdm
import puurrtybot.api.blockfrost as bbq
from puurrtybot.assets import meta

mapper_registry = registry()

Base = mapper_registry.generate_base()

engine = create_engine(f"""sqlite:///{puurrtybot.DATABASES_DIR}/pcs.db""")#, echo=True)

Session = sessionmaker()
         

@mapper_registry.mapped
@dataclass(order=True)
class Sale:
    __table__ = Table(
        "sales",
        mapper_registry.metadata,
        Column('tx_hash', String(255), primary_key=True),
        Column('asset_id', String(255), ForeignKey('assets.asset_id')),
        Column('timestamp', Integer()),
        Column('amount', Integer()),
        Column('market', String(255)),
        Column('tracked', Boolean(), default=False),
    )
    tx_hash: str = None
    asset_id: str = None
    timestamp: int = None
    amount: int = None
    market: str = None
    tracked: bool = False

        
@mapper_registry.mapped
@dataclass
class Asset:
    __table__ = Table(
        "assets",
        mapper_registry.metadata,
        Column('asset_id', String(127), primary_key=True),
        Column('address', String(255), ForeignKey('addresses.address')),
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
        Column('created_on', Integer(), default=int(datetime.utcnow().timestamp())),
        Column('updated_on', Integer(), default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()))
    )
    asset_id: str = None
    address: str = None
    policy_id: str = None
    asset_fingerprint: str = None
    initial_mint_tx_hash: str = None
    quantity: int = None
    asset_name: str = None         
    name: str = None
    prefix_name: str = None
    first_name: str = None
    last_name: str = None
    suffix_name: str = None
    img_url: str = None
    unique: str = None                      
    fur: str = None 
    hat: str = None 
    eyes: str = None 
    mask: str = None 
    tail: str = None
    hands: str = None 
    mouth: str = None 
    wings: str = None 
    outfit: str = None 
    background: str = None 
    collection: str = None 
    mint_price: int = None
    mint_time: int = None
    created_on: int = field(init=False)
    updated_on: int = field(init=False)
    sales: List[Sale] = field(default_factory=list)
        
    __mapper_args__ = {
        "properties": {
            "sales": relationship("Sale"),
        }
    }
        

@mapper_registry.mapped
@dataclass
class Address:
    __table__ = Table(
        "addresses",
        mapper_registry.metadata,
        Column('address', String(255), primary_key=True),
        Column('stake_address', String(255)),
        Column('user_id', ForeignKey('users.user_id'))
    )
    
    address: str = None
    stake_address: Optional[str] = None
    user_id: int = None
    assets: List[Asset] = field(default_factory=list)
        
    __mapper_args__ = {
        "properties": {
            "assets": relationship("Asset"),
        }
    }
    
    
@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "users",
        mapper_registry.metadata,
        Column('user_id', Integer(), primary_key=True),
        Column('balance', Integer(), default=0),
        Column('username', String(31)),
        Column('twitter_id', Integer()),
        Column('twitter_handle', String(255)),
        Column('created_on', Integer(), default=int(datetime.utcnow().timestamp())),
        Column('updated_on', Integer(), default=int(datetime.utcnow().timestamp()), onupdate=int(datetime.utcnow().timestamp()))
    )
    user_id: int = None
    username: str = None
    twitter_id: int = None
    twitter_handle: str = None
    created_on: int = field(init=False)
    updated_on: int = field(init=False)
    addresses: List[Address] = field(default_factory=list)
        
    __mapper_args__ = {
        "properties": {
            "addresses": relationship("Address"),
        }
    }
    

@mapper_registry.mapped
@dataclass   
class Listing:
    __table__ = Table(
        "listings",
        mapper_registry.metadata,
        Column('listing_id', String(255), primary_key=True),
        Column('asset_id', String(255), ForeignKey('assets.asset_id')),
        Column('timestamp', Integer()),
        Column('amount', Integer()),
        Column('market', String(255)),
        Column('tracked', Boolean(), default=False),
    )
    listing_id: str = None
    asset_id: str = None
    timestamp: int = None
    amount: int = None
    market: str = None
    tracked: bool = False  
    

@mapper_registry.mapped
@dataclass   
class Tweet:
    __table__ = Table(
        "tweets",
        mapper_registry.metadata,
        Column('tweet_id', Integer(), primary_key=True),
        Column('author_id', Integer()),
        Column('in_reply_to_user_id', Integer()),
        Column('tracked', Boolean(), default=False),
    )
    tweet_id: int = None
    author_id: int = None
    in_reply_to_user_id: int = None
    tracked: bool = False 


Base.metadata.create_all(engine)
Session = Session(bind=engine)


def initialize_assets():
    for asset in tqdm.tqdm(puurrtybot.ASSETS.values()):
        name = asset['onchain_metadata'].get('name')
        address = bbq.get_address_by_asset(asset['asset'])
        if asset['onchain_metadata'].get('unique'):
            prefix_name = first_name = last_name = suffix_name = None
        else:
            prefix_name = meta.name_has_prefix(name)
            first_name = meta.name_has_firstname(name)
            last_name = meta.name_has_lastname(name)
            suffix_name = meta.name_has_suffix(name)

        Session.add(Asset(
            asset_id = asset['asset'],
            address = address,
            policy_id = asset.get('policy_id'),
            asset_fingerprint = asset['fingerprint'],
            initial_mint_tx_hash = asset.get('initial_mint_tx_hash'),
            quantity = int(asset.get('quantity')),
            asset_name = asset.get('asset_name'),         
            name = asset['onchain_metadata'].get('name'),
            unique = asset['onchain_metadata'].get('unique'),
            prefix_name = prefix_name,
            first_name = first_name,
            last_name = last_name,
            suffix_name = suffix_name,
            img_url = asset['onchain_metadata'].get('image'),                       
            fur = asset['onchain_metadata'].get('fur'), 
            hat = asset['onchain_metadata'].get('hat'), 
            eyes = asset['onchain_metadata'].get('eyes'),  
            mask = asset['onchain_metadata'].get('mask'), 
            tail = asset['onchain_metadata'].get('tail'), 
            hands = asset['onchain_metadata'].get('hands'),  
            mouth = asset['onchain_metadata'].get('mouth'),  
            wings = asset['onchain_metadata'].get('wings'),  
            outfit = asset['onchain_metadata'].get('outfit'),  
            background = asset['onchain_metadata'].get('background'), 
            collection = asset['onchain_metadata'].get('collection'),
            mint_price = int(1_000_000*float(asset.get('mint_price'))), 
            mint_time = asset.get('mint_time'), 
            ))
    Session.commit()