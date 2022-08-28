from dataclasses import dataclass, field
from typing import List, Optional, Union

from pycardano import AddressType

from puurrtybot.pcs import metadata
    

@dataclass
class Table:
    @property
    def fields(self):
        return self.__dataclass_fields__

    @property
    def table(self):
        return self.__class__

    @property
    def primary_key(self):
        return list(self.__dataclass_fields__)[0]

    @property
    def dictionary(self):
        return {key:getattr(self, key) for key, value in self.__dataclass_fields__.items() if value.repr and value.init}


    @property
    def data(self):
        return {key:getattr(self, key) for key, value in self.__dataclass_fields__.items()}


@dataclass(order=True)
class Sale(Table):
    tx_hash: str = None
    asset_id: str = None
    action: str = None
    created_at: int = None
    confirmed_at: int = None
    buyer_address: str = None
    seller_address: str = None
    amount_lovelace: int = None
    market: str = None
    tracked: bool = True


@dataclass(order=True)
class Asset(Table):
    asset_id: str = None
    address: str = None
    address_type: AddressType = None,
    stake_address: str = None,
    stake_address_type: AddressType = None,
    policy_id: str = None
    asset_fingerprint: str = None
    initial_mint_tx_hash: str = None
    quantity: int = None
    asset_name: str = None         
    name: str = None
    prefix_name: metadata.Prefix_name = None
    first_name: metadata.First_name = None
    last_name: metadata.Last_name = None
    suffix_name: metadata.Suffix_name = None
    img_url: str = None
    unique: metadata.Unique = None                      
    fur: metadata.Fur = None 
    hat: metadata.Hat = None 
    eyes: metadata.Eyes = None 
    mask: metadata.Mask = None 
    tail: metadata.Tail = None
    hands: metadata.Hands = None 
    mouth: metadata.Mouth = None 
    wings: metadata.Wings = None 
    outfit: metadata.Outfit = None 
    background: metadata.Background = None 
    collection: str = None 
    mint_price: int = None
    mint_time: int = None
    updated_on: int = field(init=False)
    sales: List[Sale] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.background = metadata.Background(self.background)
        self.eyes = metadata.Eyes(self.eyes)
        self.fur = metadata.Fur(self.fur)
        self.hands = metadata.Hands(self.hands)
        self.hat = metadata.Hat(self.hat)
        self.mask = metadata.Mask(self.mask)
        self.mouth = metadata.Mouth(self.mouth)
        self.outfit = metadata.Outfit(self.outfit)
        self.tail = metadata.Tail(self.tail)
        self.wings = metadata.Wings(self.wings)
        self.unique = metadata.Unique(self.unique)
        self.prefix_name = metadata.Prefix_name(self.prefix_name)
        self.first_name = metadata.First_name(self.first_name)
        self.last_name = metadata.Last_name(self.last_name)
        self.suffix_name = metadata.Suffix_name(self.suffix_name)


@dataclass(order=True)
class Address(Table):
    address: str = None
    stake_address: Optional[str] = None
    user_id: int = None
    assets: List[Asset] = field(default_factory=list, repr=False)


@dataclass(order=True) 
class Listing(Table):
    listing_id: str = None
    asset_id: str = None
    created_at: int = None
    amount_lovelace: int = None
    market: str = None
    tracked: bool = True  


@dataclass(order=True)
class Role(Table):
    ix: str = field(init=False)
    role_id: int = None
    user_id: int = None
    requirement: Union[tuple, int, bool] = None
    updated_on: int = None

    def __post_init__(self):
        self.ix = f"""{self.role_id}_{self.user_id}"""
    

@dataclass(order=True)
class Tweet(Table):
    tweet_id: int = None
    created_at: int = None
    author_id: int = None
    in_reply_to_user_id: int = None
    tracked: bool = False 
    

@dataclass(order=True)
class User(Table):
    user_id: int = None
    balance: int = None
    username: str = None
    twitter_id: int = None
    twitter_handle: str = None
    updated_on: int = field(init=False)
    addresses: List[Address] = field(default_factory=list, repr=False)
    roles: List[Role] = field(default_factory=list, repr=False)
    tweets: List[Tweet] = field(default_factory=list, repr=False)