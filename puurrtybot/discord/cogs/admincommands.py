from discord.ext import commands
import discord
import puurrtybot, datetime, json
import puurrtybot.initialize.initialize as pii

SNAPSHOTS_DIR = f"""{puurrtybot.PATH}/puurrtybot/snapshots"""


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ctx = None


    @commands.command()
    async def snapshot(self, ctx):
        if ctx.channel.id == 1002510149929422858:
            self.ctx = ctx
            name = str(datetime.datetime.utcnow()).split(' ')[0]
            await ctx.send(f"""Taking snapshot_{name}, can take approx 15 minutes.""")
            pii.initialize_assets_addresses_json()
            snapshot = {}
            for key, values in puurrtybot.ASSETS_ADDRESSES.items():
                for value in values:
                    snapshot[value] = key

            with open(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json""", 'w') as openfile:
                        json.dump(snapshot, openfile)
            await self.ctx.send(file=discord.File(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json"""))


def setup(client):
    client.add_cog(AdminCommands(client))