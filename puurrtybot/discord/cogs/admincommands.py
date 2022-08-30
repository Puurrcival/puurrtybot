import asyncio, random, datetime, json

import discord
from discord import app_commands
from discord.ext import commands

from puurrtybot import PATH
import puurrtybot.api.twitter as twitter
import puurrtybot.database.query as dq

SNAPSHOTS_DIR = f"""{PATH}/puurrtybot/data/snapshots"""


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "purge", description = "Delete messages.")
    async def purge(self, interaction: discord.Interaction, limit: int):
        if interaction.user.id == 642352900357750787:
            await interaction.message.delete()
            await asyncio.sleep(1)
            await interaction.channel.purge(limit=limit)


    @app_commands.command(name = "snapshot", description = "Take a snapshot.")
    async def snapshot(self, interaction: discord.Interaction,):
        if interaction.channel.id == 1002510149929422858:
            name = str(datetime.datetime.utcnow()).split(' ')[0]
            snapshot = {}
            for asset in dq.get_asset_all():
                snapshot[asset.asset_id] = asset.address

            with open(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json""", 'w') as openfile:
                        json.dump(snapshot, openfile)
            await interaction.response(file=discord.File(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json"""))

    @app_commands.command(name = "holder_raffle", description = "Raffle holders.")
    @app_commands.choices(raffle_winners = [app_commands.Choice(name = f"{i}", value = f"{i}") for i in range(10) ])
    async def holder_raffle(self, interaction: discord.Interaction, raffle_winners: str):
        if interaction.channel_id == 1002510149929422858:
            await interaction.response.send_message(f"""{interaction.user} used /holder_raffle {raffle_winners}\nLooking for winner(s)...""" )
            assets = [asset for asset in dq.get_asset_all() if asset.address not in ['addr1w999n67e86jn6xal07pzxtrmqynspgx0fwmcmpua4wc6yzsxpljz3', 'addr1zxj47sy4qxlktqzmkrw8dahe46gtv8seakrshsqz26qnvzypw288a4x0xf8pxgcntelxmyclq83s0ykeehchz2wtspksr3q9nx']]
            content = '\n'.join([winner.address for winner in random.sample(assets, int(raffle_winners))])
            await interaction.response.send_message(content)


    @app_commands.describe(name = "twitter_raffle",temp = "value")
    @app_commands.choices(  tweet_like = [app_commands.Choice(name = name, value = value) for name, value in [("True", "True"), ("False", "False")]],
                            tweet_retweet = [app_commands.Choice(name = name, value = value) for name, value in [("True", "True"), ("False", "False")]],
                            tweeet_mentions = [app_commands.Choice(name = f"{i}", value = f"{i}") for i in range(10)],
                            raffle_winners = [app_commands.Choice(name = f"{i}", value = f"{i}") for i in range(10)]
                        )
    async def twitter_raffle(self,  interaction: discord.Interaction, tweet_id: str, tweet_like: bool, tweet_retweet: bool, tweet_mentions: int, raffle_winners: int):
        if interaction.channel.id == 1002510149929422858:
            if tweet_like == "True": tweet_like = True
            else: tweet_like = False
            if tweet_retweet == "True": tweet_retweet = True
            else: tweet_retweet = False
            winners = twitter.twitter_raffle(tweet_id = tweet_id, raffle = int(raffle_winners), minimum_mention = int(tweet_mentions), tweet_retweet = tweet_retweet, tweet_like = tweet_like)
            winners = [f"""https://twitter.com/{winner}""" for winner in winners]
            content = '\n'.join(winners)
            await interaction.response.send_message(content)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCommands(bot), guilds = [discord.Object(id = 998148160243384321)])