import random
import datetime
import asyncio

import discord
from discord import app_commands
from discord.ext import commands, tasks

from puurrtybot.database import query as dq, update as du
from puurrtybot.database.create import User
import puurrtybot.helper.functions as hf
import puurrtybot.api.twitter as twitter


VERIFY_TWEET_ID = '1549207713594343425'
VERIFY_CONVERSATION_ID = twitter.get_conversation_id_by_tweet_id(VERIFY_TWEET_ID)


class TwitterVerify:
    def __init__(self, user_id: int, twitter_handle: str, twitter_id: str):
        self.user_id = user_id
        self.twitter_handle = twitter_handle
        self.twitter_id = twitter_id
        self.amount = str(random.choice(list(range(1_000_000, 9_000_000+1))))
        self.time = hf.get_utc_time()
        
    def verify_twitter(self):
        time_limit = 70*60
        response = twitter.get_reply_from_to(f"""{self.twitter_handle}""", """PuurrtyBot""")
        try:
            if [data for data in response['data'] if data['author_id'] == self.twitter_id and self.amount in data['text'] and twitter.time_to_timestamp(data['created_at']) - hf.get_utc_time() + time_limit > 0]:
                return True
        except KeyError:
            pass

        response = twitter.get_conversation_by_conversation_id(VERIFY_CONVERSATION_ID)
        try:
            if [data for data in response['data'] if data['author_id'] == self.twitter_id and self.amount in data['text'] and twitter.time_to_timestamp(data['created_at']) - hf.get_utc_time() + time_limit > 0]:
                return True
        except KeyError:
            pass
        return False


class TwitterVerifier(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.interaction = {}
        self.verification = {}

    async def static_loop(self, user_id: int, count: int):
        print('verify started')
        interaction: discord.Interaction = self.interaction[user_id]
        self.counter[user_id] += 1
        check = self.verification[user_id].verify_twitter()
        twitter_handle = self.verification[user_id].twitter_handle
        if check:
            await interaction.followup.send(f"""<@{user_id}>, reply found, your twitter account is now verified: {twitter_handle}""", ephemeral = True)
            user: User = dq.fetch_row(User(user_id))
            user.twitter_id = self.verification[user_id].twitter_id
            user.twitter_handle = self.verification[user_id].twitter_handle
            du.update_object(user)
            self._tasks[user_id].cancel()
        elif self.counter[user_id] > count:
            await interaction.followup.send(f"""<@{user_id}>, verifying time exceeded.""", ephemeral = True)
            print('time exceeded')
        else:
            print(f"""not verified {user_id} {twitter_handle}""")
            await interaction.followup.send(f"""... still looking for reply. \n Next check for reply <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", ephemeral = True)
            self.interaction[user_id] = interaction

    def task_launcher(self, user_id, seconds, count):
        new_task = tasks.loop(seconds = seconds, count = count)(self.static_loop)
        new_task.start(user_id, count)
        self._tasks[user_id] = new_task
        self.counter[user_id] = 1


    @app_commands.command(name = "verify_twitter", description = "Verify twitter.")
    async def verify_twitter(self, interaction: discord.Interaction, *, twitter_handle: str):
        user_id = interaction.user.id
        try:    
            self._tasks[user_id].cancel()
        except KeyError:
            pass
        twitter_handle = twitter_handle.strip('@')
        twitter_id = twitter.get_twitter_id_by_username(twitter_handle)

        if dq.fetch_row(User(user_id)).twitter_id == twitter_id:
            await interaction.response.send_message(f"""{interaction.user.mention}, {twitter_handle} already verified""", ephemeral = True)
        elif not twitter_id:
             await interaction.response.send_message(f"""{interaction.user.mention}, the entered twitter name **{twitter_handle}** **doesn't exist**. Please check the spelling and try again.""", ephemeral = True)        
        else:
            self.verification[user_id] = TwitterVerify(user_id = user_id, twitter_handle = twitter_handle, twitter_id = twitter_id)
            await interaction.response.send_message(f"""**Verify a new twitter account** \n\n⌛ Please reply with **{self.verification[user_id].amount}** to https://twitter.com/PuurrtyBot/status/1549207713594343425 from **{twitter_handle}** within the next 60 minutes.\n\nWill check every 5 minutes.""", ephemeral = True)
            await asyncio.sleep(5*60)
            self.interaction[user_id] = interaction
            self.task_launcher(user_id, seconds=60*5, count=12)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TwitterVerifier(bot), guilds = [discord.Object(id = 998148160243384321)])