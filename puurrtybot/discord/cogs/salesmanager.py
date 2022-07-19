from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import puurrtybot.twitter.twitter_functions as ttf
import random, datetime, requests, puurrtybot, os, time
#import puurrtybot.blockchain.verify_queries as pbq
#import puurrtybot.database.verify_queries as pdq

HIDDEN_STATUS = True

class SalesManager(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.ctx_id = {}
        self.channel = self.client.get_channel(998321232208478219)

    async def static_loop(self, channel, quantity, task_id, count):
        print('sales running')
        market_last_100 = requests.get("""https://server.jpgstoreapis.com/collection/f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e/transactions?page=1&count=50""").json()
        buy_path = puurrtybot.PATH/"puurrtybot/databases/market_buys"
        past_buys = os.listdir(buy_path)


        one_sell = False
        for move in market_last_100['transactions'][::-1]:
            if move['tx_hash'] not in past_buys:
                if move['action']=='BUY' and move['confirmed_at']:
                    timestamp = int(datetime.datetime.strptime(move['confirmed_at'].replace('T',' ').split('+',1)[0].split('.',1)[0], '%Y-%m-%d %H:%M:%S').timestamp())
                    if timestamp - int(datetime.datetime.utcnow().timestamp()) + 70*60 > 0:
                        timestamp = timestamp + 60*60*2
                        ada = move['amount_lovelace']/1_000_000
                        asset = move['asset_id']
                        meta_name = move['display_name']
                        with open(f"""{buy_path}/{move['tx_hash']}""", 'w') as f:
                            f.write('')
                        #await channel.send(f"""{meta_name} sold for {ada}₳ at <t:{timestamp}:f>.""")
                        content=f"""{meta_name} just sold for {ada}₳!"""
                        tweet_id = ttf.tweet_sale(content, asset)
                        await channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
                        print("sent tweet")
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
        channel = self.client.get_channel(999002600013836340)
        self.task_launcher(channel, None, seconds=60)


def setup(client):
    client.add_cog(SalesManager(client))