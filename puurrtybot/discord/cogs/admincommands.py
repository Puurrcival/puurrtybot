from discord.ext import commands
import discord, random
import puurrtybot, datetime, json
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import puurrtybot.api.twitter as ttq
import puurrtybot.database.query as dq

SNAPSHOTS_DIR = f"""{puurrtybot.PATH}/puurrtybot/snapshots"""


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel = self.client.get_channel(1002510149929422858)
        self.ctx = None


    @commands.command()
    async def snapshot(self, ctx):
        if ctx.channel.id == 1002510149929422858:
            self.ctx = ctx
            name = str(datetime.datetime.utcnow()).split(' ')[0]
            snapshot = {}
            for asset in dq.get_asset_all():
                snapshot[asset.asset_id] = asset.address

            with open(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json""", 'w') as openfile:
                        json.dump(snapshot, openfile)
            await self.ctx.send(file=discord.File(f"""{SNAPSHOTS_DIR}/snapshot_{name}.json"""))


    @cog_ext.cog_slash(
        name = "holder_raffle",
        description = "holder_raffle",
        options = [
            create_option(
                            name = "raffle_winners",
                            description = "raffle_winners",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = f"{i}", value = f"{i}") for i in range(10) ]),
                   ]
                      )
    async def holder_raffle(self, ctx:SlashContext, raffle_winners: int):
        if ctx.channel.id == 1002510149929422858:
            await ctx.send(f"""{ctx.author.mention} used /holder_raffle {raffle_winners}\nLooking for winner(s)...""" )
            assets = [asset for asset in dq.get_asset_all() if asset.address not in ['addr1w999n67e86jn6xal07pzxtrmqynspgx0fwmcmpua4wc6yzsxpljz3', 'addr1zxj47sy4qxlktqzmkrw8dahe46gtv8seakrshsqz26qnvzypw288a4x0xf8pxgcntelxmyclq83s0ykeehchz2wtspksr3q9nx']]
            content = '\n'.join([winner.address for winner in random.sample(assets, int(raffle_winners))])
            await self.client.get_channel(1002510149929422858).send(content)


    @cog_ext.cog_slash(
        name = "twitter_raffle",
        description = "twitter_raffle",
        options = [
            create_option(
                            name = "tweet_id",
                            description = "tweet_id",
                            required = True,
                            option_type = 3),
            create_option(
                            name = "tweet_like",
                            description = "tweet_like",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = "True", value = "True"), create_choice(name = "False", value = "False") ]),
            create_option(
                            name = "tweet_retweet",
                            description = "tweet_retweet",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = "True", value = "True"), create_choice(name = "False", value = "False") ]),
            create_option(
                            name = "tweet_mentions",
                            description = "tweet_mentions",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = f"{i}", value = f"{i}") for i in range(10) ]),
            create_option(
                            name = "raffle_winners",
                            description = "raffle_winners",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = f"{i}", value = f"{i}") for i in range(10) ]),
                   ]
                      )
    async def twitter_raffle(self, ctx:SlashContext, tweet_id: str, tweet_like: bool, tweet_retweet: bool, tweet_mentions: int, raffle_winners: int):
        if ctx.channel.id == 1002510149929422858:
            if tweet_like == "True":
                tweet_like = True
            else:
                tweet_like = False
            if tweet_retweet == "True":
                tweet_retweet = True
            else:
                tweet_retweet = False
            winners = ttq.twitter_raffle(tweet_id = tweet_id, raffle = int(raffle_winners), minimum_mention = int(tweet_mentions), tweet_retweet = tweet_retweet, tweet_like = tweet_like)
            winners = [f"""https://twitter.com/{winner}""" for winner in winners]
            content = '\n'.join(winners)
            await self.client.get_channel(1002510149929422858).send(content)


def setup(client):
    client.add_cog(AdminCommands(client))