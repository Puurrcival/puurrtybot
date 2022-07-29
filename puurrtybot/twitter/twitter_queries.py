import datetime, puurrtybot, requests, puurrtybot.databases.database_functions as ddf, random
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


def get_user_by_id(twitter_id: str) -> str:
    try:
        return requests.request("GET", url = f"{network}/users/{twitter_id}""", headers=headers).json()['data']['username']
    except KeyError:
        return False


def get_conversation_id_by_tweet_id(tweet_id: str) -> str:
    return requests.request("GET", url = f"{network}/tweets/{tweet_id}?tweet.fields=conversation_id", headers=headers).json()['data']['conversation_id']


def get_conversation_by_conversation_id(conversation_id: str):
    return requests.request("GET", f"""{network}/tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at""", headers=headers).json()


def get_reply_from_to(from_user, to_user):
    return requests.request("GET", f"""{network}/tweets/search/recent?query=from:{from_user} to:{to_user}&tweet.fields=author_id,created_at""", headers=headers).json()


def get_mentions_puurrtycats():
        return requests.request("GET", f"""{network}/users/1479912806866694149/mentions?tweet.fields=in_reply_to_user_id,author_id""", headers=headers).json()


def get_untracked_mentions_puurrtycats():
    untracked_mentions = []
    try:
        tweets = get_mentions_puurrtycats()['data']
        for tweet in tweets:
            try:
                tweet['in_reply_to_user_id']
            except KeyError:
                try:
                    puurrtybot.TWITTER_MENTIONS[tweet['id']]
                except KeyError:
                    untracked_mentions.append(tweet)
            puurrtybot.TWITTER_MENTIONS[tweet['id']] = tweet
        ddf.save_twitter_mentions()
    except KeyError:
        pass        
    return untracked_mentions


def get_twitter_id_list_by_retweet(tweet_id):
    users_retweeted = []
    next_token=""
    while True:
        response = requests.request("GET", f"""{network}/tweets/{tweet_id}/retweeted_by?{next_token}tweet.fields=author_id""", headers=headers).json()
        try:
            users_retweeted += [entity['id'] for entity in response['data']] 
            next_token = response['meta']['next_token']
            next_token = f"""pagination_token={next_token}&"""
        except KeyError:
            break;
    return users_retweeted


def get_twitter_id_list_by_liking(tweet_id):
    users_liking = []
    next_token=""
    while True:
        response = requests.request("GET", f"""{network}/tweets/{tweet_id}/liking_users?{next_token}tweet.fields=author_id""", headers=headers).json()
        try:
            users_liking += [entity['id'] for entity in response['data']] 
            next_token = response['meta']['next_token']
            next_token = f"""pagination_token={next_token}&"""
        except KeyError:
            break;
    return users_liking


def get_twitter_id_list_by_reply_mention(tweet_id, minimum_mention = 0):
    conversation_id = requests.request("GET", url = f"{network}/tweets/{tweet_id}?tweet.fields=conversation_id", headers=headers).json()['data']['conversation_id']
    data = []
    next_token=""
    max_results = 100
    while True:
        response = requests.request("GET", f"""{network}/tweets/search/recent?{next_token}max_results={max_results}&query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at&expansions=entities.mentions.username""", headers=headers).json()
        data += response['data']
        try:
            next_token = response['meta']['next_token']
            next_token = f"""next_token={next_token}&"""
        except KeyError:
            break;
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