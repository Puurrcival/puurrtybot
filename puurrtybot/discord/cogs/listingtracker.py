import discord
from discord.ext import commands, tasks
import time
import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi
import requests
import puurrtybot.functions as pf
from puurrtybot import POLICY_PCS


class ListingTracker(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('ListingsTracker running')
        untracked_listings = []
        last_listing = requests.get(f"""https://server.jpgstoreapis.com/search/tokens?policyIds=[%22{POLICY_PCS}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size=1""").json()['tokens'][0]
        if not ddq.get_listing_by_id(f"""{last_listing['listed_at']}_{last_listing['asset_name']}"""):
            listings = requests.get(f"""https://server.jpgstoreapis.com/search/tokens?policyIds=[%22{POLICY_PCS}%22]&saleType=buy-now&sortBy=recently-listed&traits=%7B%7D&nameQuery=&verified=default&pagination=%7B%7D&size=300""").json()['tokens']
            for listing in listings:
                if ddq.get_listing_by_id(f"""{listing['listed_at']}_{listing['asset_name']}"""):
                    break;
                else:
                    untracked_listings.append( (f"""{listing['listed_at']}_{listing['asset_name']}""" , listing) )

        untracked_listings.reverse()
        for listing_id, listing in untracked_listings:
            timestamp = pf.time_to_timestamp(listing['created_at'].split('.')[0].split('+')[0].replace('T',' '))
            ddi.listing_new(listing_id = listing_id, asset_id = listing['asset_name'], timestamp = timestamp, amount = int(listing['listing_lovelace']), tracked = False)

        new_listings = ddq.get_listings()
        for listing in new_listings:
            asset = ddq.get_asset_by_id(listing.asset_id)
            display_name = asset.name
            embed=discord.Embed(title=f"""{display_name} just listed for {listing.amount/1_000_000}₳!""", url=f"""https://www.jpg.store/asset/{listing.asset_id}""", description="", color=0x109319)
            embed.set_image(url=f"""https://ipfs.io/ipfs/{asset.img_url.split('/')[-1]}""")
            await self.channel.send(embed=embed)
            ddi.listing_tracked(listing.listing_id)
            time.sleep(1)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(ListingTracker(client))