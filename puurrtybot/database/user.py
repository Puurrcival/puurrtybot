from dataclasses import dataclass, field
from typing import List

from puurrtybot.database.address import Address

@dataclass
class User:
    user_id: int = None
    username: str = None
    twitter_id: int = None
    twitter_handle: str = None
    updated_on: int = field(init=False)
    addresses: List[Address] = field(default_factory=list)
