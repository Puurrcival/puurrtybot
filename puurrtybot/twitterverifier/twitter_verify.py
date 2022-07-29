import puurrtybot.functions as f
import os, puurrtybot, json, random
import puurrtybot.twitter.twitter_queries as ttq
verify_tweet_id = '1549207713594343425'
verify_conversation_id = ttq.get_conversation_id_by_tweet_id(verify_tweet_id)

class TwitterVerify:
    def __init__(self, user_id: int, twitter_handle: str, twitter_id: str, from_log: bool = False):
        self.user_id = user_id
        self.twitter_handle = twitter_handle
        self.twitter_id = twitter_id
        self.log_path = f"""{puurrtybot.DATABASES_DIR}/verify_twitter/{self.user_id}.json"""
        if from_log:
            self.read_log()
        else:
            self.new_verify()


    def read_log(self):
        with open(f"""{self.log_path}.json""", 'r') as json_file:
            log_data = json.load(json_file)
            if log_data['time'] + 1*1*60*60 - f.get_utc_time() > 0:
                self.twitter_handle = log_data['twitter_handle']
                self.amount = log_data['amount']
                self.user_id = log_data['user_id']
                self.time = log_data['time']
            else:
                self.delete_log()

    
    def create_log(self):
        with open(self.log_path, 'w') as json_file:
                json.dump({'twitter_handle': self.twitter_handle,
                           'amount' : self.amount,
                           'user_id' : self.user_id,
                           'time' : self.time}, json_file)


    def delete_log(self):
        os.unlink(self.log_path)


    def new_verify(self):
        self.amount = str(random.choice(list(range(1_000_000, 9_000_000+1))))
        self.time = f.get_utc_time()
        self.create_log()

        
    def verify_twitter(self):
        time_limit = 70*60
        response = ttq.get_reply_from_to(f"""{self.twitter_handle}""", """PuurrtyBot""")
        try:
            if [data for data in response['data'] if data['author_id'] == self.twitter_id and self.amount in data['text'] and ttq.twitter_time_to_timestamp(data['created_at']) - f.get_utc_time() + time_limit > 0]:
                return True
        except KeyError:
            pass

        response = ttq.get_conversation_by_conversation_id(verify_conversation_id)
        try:
            if [data for data in response['data'] if data['author_id'] == self.twitter_id and self.amount in data['text'] and ttq.twitter_time_to_timestamp(data['created_at']) - f.get_utc_time() + time_limit > 0]:
                return True
        except KeyError:
            pass
        return False


def get_interrupted_verification():
    return os.listdir(f"""{puurrtybot.DATABASES_DIR}/verify_twitter/{self.user_id}.json""")