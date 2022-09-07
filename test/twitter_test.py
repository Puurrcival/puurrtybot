# Testing twitter api
import puurrtybot.api.twitter as twitter

TWITTERHANDLE = "@puurrtybot"
TWITTER_ID = 1534161469805404162
TWEET_ID = 1549207713594343425


def test_get_id_by_user():
    # exists
    assert TWITTER_ID == twitter.get_twitter_id_by_username(TWITTERHANDLE)

    # exists not
    assert not twitter.get_twitter_id_by_username("pu33rtyb0tdo")


def test_get_user_by_id():
    # exists
    assert TWITTERHANDLE.strip('@').lower() == twitter.get_username_by_twitter_id(TWITTER_ID)


def test_get_conversation_id_by_tweet_id():
    assert TWEET_ID == twitter.get_conversation_id_by_tweet_id(TWEET_ID)
    

def test_get_conversation_by_conversation_id():
    assert type(twitter.get_conversation_by_conversation_id(TWEET_ID)['meta']) is dict


def test_get_reply_from_to():
    assert type(twitter.get_reply_from_to(TWITTERHANDLE, TWITTERHANDLE)) is dict


def test_get_mentions_by_twitter_id():
    assert type(twitter.get_untracked_mentions_by_twitter_id(TWITTER_ID)) is list