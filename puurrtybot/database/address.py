from dataclasses import dataclass, field
from typing import List, Optional

from puurrtybot.pcs.asset import Asset

@dataclass
class Address:
    address: str = None
    stake_address: Optional[str] = None
    user_id: int = None
    assets: List[Asset] = field(default_factory=list)