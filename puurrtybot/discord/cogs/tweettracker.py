from discord.ext import commands, tasks

import puurrtybot.database.query as dq
from puurrtybot.database.update import update_balance_by_user_id
from puurrtybot.pcs import TWITTER_ID
from puurrtybot.database.insert import insert_object
from puurrtybot.api import twitter


class TweetTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('TweetTracker running')
        if not dq.get_tweet_by_tweet_id(twitter.get_mentions_by_twitter_id_last(TWITTER_ID).tweet_id):
            tweets = twitter.get_untracked_mentions_by_twitter_id(TWITTER_ID)      

            for tweet in tweets:
                if not tweet.in_reply_to_user_id:
                    user = dq.get_user_by_twitter_id(tweet.author_id)
                    if user:
                        amount = 5000
                        await self.channel.send(f"""<@{user.user_id}> got rewarded with {amount} Coins for tweeting:\n https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
                        update_balance_by_user_id(user.user_id, amount)                
                    else:
                        await self.channel.send(f"""https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
                insert_object(tweet)
                print("tracked tweet")
        
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999043361983955116)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(TweetTracker(client))