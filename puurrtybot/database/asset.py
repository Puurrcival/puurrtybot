from dataclasses import dataclass, field
from typing import List

from puurrtybot.database.sale import Sale

@dataclass
class Asset:
    asset_id: str = None
    address: str = None
    address_type: str = None,
    stake_address: str = None,
    stake_address_type: str = None,
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
    updated_on: int = field(init=False)
    sales: List[Sale] = field(default_factory=list)