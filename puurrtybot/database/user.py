from dataclasses import dataclass, field
from typing import List

from puurrtybot.database.address import Address
from puurrtybot.database.tweet import Tweet
from puurrtybot.pcs.role import Role


@dataclass
class User:
    user_id: int = None
    balance: int = None
    username: str = None
    twitter_id: int = None
    twitter_handle: str = None
    updated_on: int = field(init=False)
    addresses: List[Address] = field(default_factory=list)
    roles: List[Role] = field(default_factory=list)
    tweets: List[Tweet] = field(default_factory=list)
