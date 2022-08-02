import discord
from discord.ext import commands, tasks
import time, puurrtybot.twitter.twitter_functions as ttf, puurrtybot.markets.market_queries as mmq, puurrtybot, datetime
import puurrtybot.assets.get_functions as agf


class ListingsTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('ListingsTracker running')
        new_listings = mmq.get_untracked_listings_jpgstore()

        for listing_id, value in new_listings.items():
            display_name = puurrtybot.ASSETS[value['asset']]['onchain_metadata']['name']
            embed=discord.Embed(title=f"""{display_name} just listed for {value['amount']}₳!""", url=f"""https://www.jpg.store/asset/{value['asset']}""", description="", color=0x109319)
            embed.set_image(url=f"""https://infura-ipfs.io/ipfs/{puurrtybot.ASSETS[value['asset']]['onchain_metadata']['image'].split('/')[-1]}""")
            await self.channel.send(embed=embed)
            time.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(ListingsTracker(client))