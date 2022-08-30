import discord
from discord.ext import commands, tasks

from puurrtybot.database import query as dq, insert as di
from puurrtybot.api import jpgstore
from puurrtybot.pcs import POLICY_ID
from puurrtybot.helper.asset_profile import AssetProfile

class ListingTracker(commands.Cog):
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot


    async def static_loop(self):
        print('ListingsTracker running')
        if not dq.fetch_row(jpgstore.get_listing_last(POLICY_ID)):
            listings = jpgstore.get_listings_untracked(POLICY_ID)
            listings.sort(key=lambda x: x.created_at, reverse=False)
            for listing in listings:
                ap = AssetProfile(listing.asset_id)
                embed, embed_files = ap.embed_short
                embed.title=f"""{ap.asset_name} just listed for {listing.amount_lovelace/1_000_000}₳!"""
                embed.url = f"""https://www.jpg.store/asset/{listing.asset_id}"""
                di.insert_row(listing)
                await self.channel.send(embed=embed, files=embed_files)


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.bot.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ListingTracker(bot), guilds = [discord.Object(id = 998148160243384321)])