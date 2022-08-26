import tweepy

from puurrtybot.helper.image_handle import get_asset_image
from puurrtybot import TWITTER_KEY, TWITTER_KEY_SECRET, TWITTER_BEARER_TOKEN, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

client = tweepy.Client(TWITTER_BEARER_TOKEN, TWITTER_KEY, TWITTER_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(TWITTER_KEY, TWITTER_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(auth)


def tweet_sale(content, asset):
    image_stream = get_asset_image(asset)
    ret = tweepy_api.media_upload(filename="cat", file=image_stream)
    temp = tweepy_api.update_status(media_ids=[ret.media_id_string], status=content)
    return temp.id