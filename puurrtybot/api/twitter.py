# https://developer.twitter.com/apitools/api

import datetime
import random

import requests
from requests.models import Response

import puurrtybot
import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi
HEADERS = {"Authorization": "Bearer {}".format(puurrtybot.TWITTER_BEARER_TOKEN)}
NETWORK = 'https://api.twitter.com/2'


TWITTER_STATUS_CODES = { 
    # https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
    304: """Not Modified""",
    400: """Bad Request""",
    401: """Unauthorized""",
    403: """Forbidden""",
    404: """Not Found""",
    406: """Not Acceptable""",
    410: """Gone""",
    422: """Unprocessable Entity""",
    429: """Too Many Requests""",
    500: """Internal Server Error""",
    502: """Bad Gateway""",
    503: """Service Unavailable""",
    504: """Gateway Timeout"""}


def query(query_string: str) -> Response:
    response = requests.get(f"""{NETWORK}{query_string}""", headers=HEADERS)
    if response.status_code != 200:
        raise Exception( (response.status_code, f"""{TWITTER_STATUS_CODES[response.status_code]}""") )
    return response


def twitter_time_to_timestamp(timeformat) -> int:
    return int(datetime.datetime.strptime(timeformat.split('.')[0].replace('T', ' '),"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def get_id_by_user(name: str) -> int:
    try:
        return int(query(f"""/users/by/username/{name.strip('@')}""").json()['data']['id'])
    except KeyError:
        return False


def get_user_by_id(twitter_id: int) -> str:
    try:
        return query(f"""/users/{twitter_id}""").json()['data']['username'].lower()
    except KeyError:
        return False


def get_conversation_id_by_tweet_id(tweet_id: int) -> int:
    return int(query(f"""/tweets/{tweet_id}?tweet.fields=conversation_id""").json()['data']['conversation_id'])


def get_conversation_by_conversation_id(conversation_id: str) -> dict:
    return query(f"""/tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at""").json()


def get_reply_from_to(from_user, to_user) -> dict:
    return query(f"""/tweets/search/recent?query=from:{from_user.strip('@')} to:{to_user.strip('@')}&tweet.fields=author_id,created_at""").json()


def get_mentions_by_twitter_id(twitter_id: int, next_token: str ="") -> dict:
    return query(f"""/users/{twitter_id}/mentions?{next_token}tweet.fields=in_reply_to_user_id,author_id""").json()


def store_untracked_mentions_by_tweet_id(twitter_id: int, max_count: int = -1) -> None:
    next_token=""
    while max_count != 0:
        max_count += -1
        response = get_mentions_by_twitter_id(twitter_id, next_token)
        try:
            for entity in response['data']:
                in_reply_to_user_id = entity.get('in_reply_to_user_id', None)
                tweet_id , author_id = int(entity['id']), int(entity['author_id'])
                if not ddq.get_tweet_by_id(tweet_id):
                    ddi.tweet_new(tweet_id, author_id, in_reply_to_user_id = in_reply_to_user_id, tracked = False)
                else:
                    max_count = 0
                    break          
            next_token = response['meta']['next_token']
            next_token = f"""pagination_token={next_token}&"""
        except KeyError:
            break 


def get_twitter_id_list_by_retweet(tweet_id, max_count = -1):
    users_retweeted = []
    next_token=""
    while max_count != 0:
        max_count += -1
        response = query(f"""/tweets/{tweet_id}/retweeted_by?{next_token}tweet.fields=author_id""").json()
        try:
            users_retweeted += [entity['id'] for entity in response['data']] 
            next_token = response['meta']['next_token']
            next_token = f"""pagination_token={next_token}&"""
        except KeyError:
            break
    return users_retweeted


def get_twitter_id_list_by_liking(tweet_id, max_count = -1):
    users_liking = []
    next_token=""
    while max_count != 0:
        max_count += -1
        response = query(f"""/tweets/{tweet_id}/liking_users?{next_token}tweet.fields=author_id""").json()
        try:
            users_liking += [entity['id'] for entity in response['data']] 
            next_token = response['meta']['next_token']
            next_token = f"""pagination_token={next_token}&"""
        except KeyError:
            break
    return users_liking


def get_twitter_id_list_by_reply_mention(tweet_id, minimum_mention = 0):
    conversation_id = query(f"/tweets/{tweet_id}?tweet.fields=conversation_id").json()['data']['conversation_id']
    data = []
    next_token=""
    max_results = 100
    while True:
        response = query(f"""/tweets/search/recent?{next_token}max_results={max_results}&query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at&expansions=entities.mentions.username""").json()
        data += response['data']
        try:
            next_token = response['meta']['next_token']
            next_token = f"""next_token={next_token}&"""
        except KeyError:
            break
    return [d['author_id'] for d in data if len(set([mention['id'] for mention in d['entities']['mentions']])) >= minimum_mention]


def twitter_raffle(tweet_id, raffle = 1, minimum_mention = 3, tweet_retweet = True, tweet_like=True):
    mentions = get_twitter_id_list_by_reply_mention(tweet_id, minimum_mention = minimum_mention)
    if tweet_retweet:
        retweets = get_twitter_id_list_by_retweet(tweet_id)
        eligible = set(mentions).intersection(retweets)
    if tweet_like:
        likes = get_twitter_id_list_by_liking(tweet_id)
        eligible = set(eligible).intersection(likes)
    eligible = list(set(eligible))
    return [get_user_by_id(twitter_id) for twitter_id in random.sample(eligible, raffle)]