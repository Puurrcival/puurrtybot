import datetime, puurrtybot, requests

headers = {"Authorization": "Bearer {}".format(puurrtybot.TWITTER_BEARER_TOKEN)}

def get_id_by_user(name):
    try:
        url = f"""https://api.twitter.com/2/users/by/username/{name}"""
        return requests.request("GET", url, headers=headers).json()['data']['id']
    except KeyError:
        return False

def twitter_time_2_utc_timestamp(twitter_time):
    datetime_str = twitter_time.replace('T', ' ').strip('Z')
    return int(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f').timestamp())


def verify_twitter(name, text, tweet_id="1549207713594343425"):
    time_limit = 70*60
    user_id = get_id_by_user(name)
    if user_id:
        url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=conversation_id"
        conversation_id = requests.request("GET", url, headers=headers).json()['data']['conversation_id']
        url = f"""https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{conversation_id}&tweet.fields=author_id,created_at"""
        response = requests.request("GET", url, headers=headers).json()
        try:
            if [data for data in response['data'] if data['author_id'] == user_id and text in data['text'] and twitter_time_2_utc_timestamp(data['created_at']) - int(datetime.datetime.utcnow().timestamp()) + time_limit > 0]:
                return True
            else:
                return False
        except KeyError:
            return False
    else:
        return False