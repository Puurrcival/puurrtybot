import discord
from discord.ext import commands, tasks

import puurrtybot.database.query as dq
import puurrtybot.database.insert as di
from puurrtybot.api import jpgstore
from puurrtybot.database.create import session
from puurrtybot.pcs import POLICY_ID

class ListingTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('ListingsTracker running')

        if not dq.get_listing_by_id(jpgstore.get_listing_last(POLICY_ID).listing_id):
            listings = jpgstore.get_listings_untracked(POLICY_ID)
            listings.sort(key=lambda x: x.created_at, reverse=True)

            for listing in listings:        
                session.add(listing)
                session.commit()
                asset = dq.get_asset_by_asset_id(listing.asset_id)
                display_name = asset.name
                embed=discord.Embed(title=f"""{display_name} just listed for {listing.amount_lovelace/1_000_000}₳!""", url=f"""https://www.jpg.store/asset/{listing.asset_id}""", description="", color=0x109319)
                embed.set_image(url=f"""https://ipfs.io/ipfs/{asset.img_url.split('/')[-1]}""")
                di.new_listing(listing.listing_id)
                await self.channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(ListingTracker(client))