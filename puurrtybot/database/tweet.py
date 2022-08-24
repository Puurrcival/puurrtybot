from dataclasses import dataclass

@dataclass   
class Tweet:
    tweet_id: int = None
    created_at: int = None
    author_id: int = None
    in_reply_to_user_id: int = None
    tracked: bool = False 