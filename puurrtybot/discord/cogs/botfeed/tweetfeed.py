import discord
from discord.ext import commands, tasks

from puurrtybot.database import query as dq, insert as di, update as du
from puurrtybot.pcs import TWITTER_ID
from puurrtybot.api import twitter
from puurrtybot.database.create import User

class TweetFeed(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client

    async def static_loop(self):
        try:
            print('TweetFeed running')
            if not dq.get_tweet_by_tweet_id(twitter.get_mentions_by_twitter_id_last(TWITTER_ID).tweet_id):
                new_tweets = twitter.get_untracked_mentions_by_twitter_id(TWITTER_ID)      

                for tweet in new_tweets:
                    di.insert_row(tweet)
                    if not tweet.in_reply_to_user_id:
                        user = dq.fetch_row_by_value(User, 'twitter_id', tweet.author_id)
                        if user:
                            amount = 5000
                            await self.channel.send(f"""<@{user.user_id}> got rewarded with {amount} Coins for tweeting:\n https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
                            user.balance += amount
                            du.update_object(user)                
                        else:
                            await self.channel.send(f"""https://twitter.com/{tweet.author_id}/status/{tweet.tweet_id}""")
                    print("tracked tweet")
        except Exception as e:
            print(f"""TwwetFeed error occured: {e.message}""")

        
    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999043361983955116)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(TweetFeed(client), guilds = [discord.Object(id = 998148160243384321)])