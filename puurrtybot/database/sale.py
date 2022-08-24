from dataclasses import dataclass

@dataclass(order=True)
class Sale:
    tx_hash: str = None
    asset_id: str = None
    action: str = None
    created_at: int = None
    confirmed_at: int = None
    buyer_address: str = None
    seller_address: str = None
    amount_lovelace: int = None
    market: str = None
    tracked: bool = None