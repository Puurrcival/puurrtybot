from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import puurrtybot.twitter.twitter_functions as ttf
import puurrtybot.twitter.verify_twitter as tvt
import datetime, puurrtybot, requests, os, time

headers = {"Authorization": "Bearer {}".format(puurrtybot.TWITTER_BEARER_TOKEN)}
url =f"""https://api.twitter.com/2/users/1479912806866694149/mentions?tweet.fields=in_reply_to_user_id,author_id"""

HIDDEN_STATUS = True

class TwitterTracker(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.ctx_id = {}
        self.channel = self.client.get_channel(998321232208478219)

    async def static_loop(self, channel, quantity, task_id, count):
        print('twitter running')
        r = requests.request("GET", url, headers=headers).json()

        buy_path = puurrtybot.PATH/"puurrtybot/databases/twitter_mentions"
        past_buys = os.listdir(buy_path)


        one_sell = False
        for tweet in r['data'][::-1]:
            try:
                tweet['in_reply_to_user_id']
            except KeyError:
                if tweet['id'] not in past_buys:
                    author = tweet['author_id']
                    
                    with open(f"""{buy_path}/{tweet['id']}""", 'w') as f:
                        f.write('')
                    await channel.send(f"""https://twitter.com/{author}/status/{tweet['id']}""")
                    print("tracked tweet")
                    time.sleep(5)
        #if not one_sell:
        #    await channel.send(f"""No new sales""")
        

    def task_launcher(self, channel, quantity, seconds=5, count=None):
        new_task = tasks.loop(seconds=seconds, count = count)(self.static_loop)
        new_task.start(channel, quantity, self.task_n, count)
        self._tasks[self.task_n] = (new_task, channel, quantity, self.task_n)
        self.counter[self.task_n] = 1
        self.task_n += 1
        

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.client.get_channel(999043361983955116)
        self.task_launcher(channel, None, seconds=180)


def setup(client):
    client.add_cog(TwitterTracker(client))