from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import datetime, puurrtybot
import puurrtybot.api.twitter as ttq
import puurrtybot.twitterverifier.twitter_verify as tvt


import puurrtybot.databases.database_queries as ddq
import puurrtybot.databases.database_inserts as ddi

HIDDEN_STATUS = True


class TwitterVerifier(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.ctx_id = {}
        self.verification = {}


    async def static_loop(self, user_id, count):
        print('verify started')
        ctx = self.ctx_id[user_id]
        self.counter[user_id] += 1
        check = self.verification[user_id].verify_twitter()
        twitter_handle = self.verification[user_id].twitter_handle
        if check:
            await ctx.send(f"""<@{user_id}>, reply found, your twitter account is now verified: {twitter_handle}""", hidden=HIDDEN_STATUS)
            ddi.user_change_twitter(user_id, self.verification[user_id].twitter_id, self.verification[user_id].twitter_handle)
            self._tasks[user_id].cancel()
        elif self.counter[user_id] > count:
            await ctx.send(f"""<@{user_id}>, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')
        else:
            print(f"""not verified {user_id} {twitter_handle}""")
            await ctx.send(f"""... still looking for reply. \n Next check for reply <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
            self.ctx_id[user_id] = ctx
            

    def task_launcher(self, user_id, seconds, count):
        new_task = tasks.loop(seconds = seconds, count = count)(self.static_loop)
        new_task.start(user_id, count)
        self._tasks[user_id] = new_task
        self.counter[user_id] = 1
        

    @cog_ext.cog_slash(
        name = "verify_twitter",
        description = "verify_twitter",
        options = [
            create_option(
                            name = "twitter_handle",
                            description = "twitter_handle",
                            required = True,
                            option_type = 3)
                   ]
                      )
    async def verify_task(self, ctx:SlashContext, twitter_handle:str):
        user_id = ctx.author_id
        try:    
            self._tasks[user_id].cancel()
        except KeyError:
            pass
        twitter_handle = twitter_handle.strip('@')
        twitter_id = ttq.get_id_by_user(twitter_handle)

        if ddq.get_user_by_id(user_id).twitter_id:
            await ctx.send(f"""{ctx.author.mention}, {twitter_handle} already verified""", hidden=HIDDEN_STATUS)
        elif not twitter_id:
             await ctx.send(f"""{ctx.author.mention}, the entered twitter name **{twitter_handle}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)        
        else:
            self.verification[user_id] = tvt.TwitterVerify(user_id = user_id, twitter_handle = twitter_handle, twitter_id = twitter_id)
            await ctx.send(f"""**Verify a new twitter account** \n\n⌛ Please reply with **{self.verification[user_id].amount}** to https://twitter.com/PuurrtyBot/status/1549207713594343425 from **{twitter_handle}** within the next 60 minutes.""", hidden=HIDDEN_STATUS)
            self.ctx_id[user_id] = ctx
            self.task_launcher(user_id, seconds=60*5, count=12)


def setup(client):
    client.add_cog(TwitterVerifier(client))