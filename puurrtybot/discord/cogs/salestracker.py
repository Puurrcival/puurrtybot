from discord.ext import commands, tasks
import time, puurrtybot.twitter.twitter_functions as ttf, puurrtybot.markets.market_queries as mmq


class SalesTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('SalesTracker running')
        new_sales = mmq.get_untracked_sales_jpgstore()

        for sale in new_sales:
            display_name = puurrtybot.ASSETS[sale['asset']]['onchain_metadata']['name']
            content=f"""{display_name} just sold for {sale['amount']}₳!"""
            tweet_id = ttf.tweet_sale(content, sale['asset'])
            await self.channel.send(f"""https://twitter.com/PuurrtyBot/status/{tweet_id}""")
            print("sent sale tweet")
            time.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(999002600013836340)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(SalesTracker(client))