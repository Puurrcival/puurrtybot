from dataclasses import dataclass

@dataclass   
class Listing:
    listing_id: str = None
    asset_id: str = None
    created_at: int = None
    amount_lovelace: int = None
    market: str = None
    tracked: bool = False  
    