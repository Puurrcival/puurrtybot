import discord
from discord.ext import commands, tasks
import puurrtybot.blockfrost.blockfrost_queries as bbq
import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi
import puurrtybot.functions as func


class UpdateManager(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def static_loop(self):
        print('UpdateManager running')
        outdated_assets = ddq.get_asset_all(func.get_utc_time()-24*60*60)
        for asset in outdated_assets:
            address = bbq.get_address_by_asset(asset.asset_id)
            ddi.asset_change_address(asset.asset_id, address)

        if outdated_assets:
            print('Updated Assets')
        


    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 10*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(UpdateManager(client))