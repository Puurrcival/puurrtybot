import datetime, puurrtybot, requests
headers = {"Authorization": "Bearer {}".format(puurrtybot.TWITTER_BEARER_TOKEN)}
network = 'https://api.twitter.com/2'

# https://developer.twitter.com/apitools/api
# https://developer.twitter.com/en/support/twitter-api/error-troubleshooting
twitter_http_codes = { 
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


def twitter_time_to_timestamp(timeformat):
    return int(datetime.datetime.strptime(timeformat.split('.')[0].replace('T', ' '),"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def get_id_by_user(name: str) -> str:
    try:
        return requests.request("GET", f"""{network}/users/by/username/{name}""", headers=headers).json()['data']['id']
    except KeyError:
        return False


def get_conversation_id_by_tweet_id(tweet_id: str) -> str:
    return requests.request("GET", url = f"{network}/tweets/{tweet_id}?tweet.fields=conversation_id", headers=headers).json()['data']['conversation_id']


def get_conversation_by_conversation_id(conversation_id: str):
    return requests.request("GET", f"""{network}/tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at""", headers=headers).json()


def get_reply_from_to(from_user, to_user):
    return requests.request("GET", f"""{network}/tweets/search/recent?query=from:{from_user} to:{to_user}&tweet.fields=author_id,created_at""", headers=headers).json()
