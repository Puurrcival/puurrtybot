from discord.ext import commands, tasks
import puurrtybot.twitter.twitter_queries as ttq, time

class TwitterTracker(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('TwitterTracker running')
        new_tweets = ttq.get_untracked_mentions_puurrtycats()
        for tweet in new_tweets:
            await self.channel.send(f"""https://twitter.com/{tweet['author_id']}/status/{tweet['id']}""")
            print("tracked tweet")
            time.sleep(1)
        

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999043361983955116)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(TwitterTracker(client))