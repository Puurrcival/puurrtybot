import random
import datetime
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from puurrtybot.database import query as dq, update as du
from puurrtybot.database.create import User
import puurrtybot.helper.functions as hf
import puurrtybot.api.twitter as twitter


VERIFY_TWEET_ID = '1549207713594343425'
VERIFY_CONVERSATION_ID = twitter.get_conversation_id_by_tweet_id(VERIFY_TWEET_ID)


async def verify_twitter(user, amount, time_window):
    response = twitter.get_reply_from_to(f"""{user.twitter_handle}""", """PuurrtyBot""")
    try:
        if [data for data in response['data'] if data['author_id'] == user.twitter_id and amount in data['text'] and twitter.time_to_timestamp(data['created_at']) - hf.get_utc_time() + time_window > 0]:
            return True
    except KeyError:
        pass
    response = twitter.get_conversation_by_conversation_id(VERIFY_CONVERSATION_ID)
    try:
        if [data for data in response['data'] if data['author_id'] == user.twitter_id and amount in data['text'] and twitter.time_to_timestamp(data['created_at']) - hf.get_utc_time() + time_window > 0]:
            return True
    except KeyError:
        pass
    return False


class TwitterVerifier(commands.Cog):
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot

    @app_commands.command(name = "verify_twitter", description = "Verify twitter.")
    async def verify_twitter(self, interaction: discord.Interaction, *, twitter_handle: str):
        ctx: commands.Context = await commands.Context.from_interaction(interaction)
        twitter_handle = twitter_handle.strip('@ ')
        twitter_id = twitter.get_twitter_id_by_username(twitter_handle)
        if not twitter_id:
            content = f"""{interaction.user.mention}, the entered twitter handle <**{twitter_handle}**> **doesn't exist**. Please check the spelling and try again."""
        elif dq.fetch_row_by_value(User, User().column.twitter_id, twitter_id):
            print(dq.fetch_row_by_value(User, User().column.twitter_id, twitter_id))
            content = f"""{interaction.user.mention}, this twitter handle has been verified already: **{twitter_handle}**"""
        else:
            amount = random.choice(list(range(2_000_000, 3_000_000+1)))
            content = f"""**Verify a new twitter account** \n\n⌛ Please reply with **{amount}** to https://twitter.com/PuurrtyBot/status/1549207713594343425 from **{twitter_handle}** within the next 60 minutes.\n\nWill check every 5 minutes."""
        await interaction.response.send_message(content, ephemeral = True)

        amount = None
        time_window = 3*60
        if amount:
            user: User = dq.fetch_row(User(interaction.user.id))
            user.twitter_id, user.twitter_handle = twitter_id, twitter_handle
            await asyncio.sleep(time_window)

            message = await ctx.send(f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""", ephemeral=True)
            for _ in range(20):
                if await verify_twitter(user, amount, time_window):
                    du.update_object(user)
                    if not interaction.is_expired(): await message.edit(content = f"""Verification of **{user.twitter_handle}** successful.""") 
                    break
                await asyncio.sleep(time_window)
                if not interaction.is_expired(): await message.edit(content = f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""")
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TwitterVerifier(bot), guilds = [discord.Object(id = 998148160243384321)])