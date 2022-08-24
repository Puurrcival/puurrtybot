from discord.ext import commands, tasks
import puurrtybot.api.twitter as ttq, time
import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi
from puurrtybot import TWITTER_ID

from puurrtybot.database.create import Session

class TweetTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('TweetTracker running')
        tweets = ttq.get_untracked_mentions_by_twitter_id(TWITTER_ID)

        for tweet in tweets:
            if not tweet.in_reply_to_user_id:
                user = ddq.get_user_by_twitter_id(tweet.author_id)
                if user:
                    amount = 5000
                    await self.channel.send(f"""<@{user.user_id}> got rewarded with {amount} Coins for tweeting:\n https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
                    ddi.user_change_balance(user.user_id, amount)                
                else:
                    await self.channel.send(f"""https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
            Session.add(tweet)
            Session.commit()
            print("tracked tweet")
            time.sleep(1)
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999043361983955116)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(TweetTracker(client))