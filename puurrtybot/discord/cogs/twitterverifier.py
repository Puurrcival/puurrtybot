from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import random, datetime
import puurrtybot
import puurrtybot.blockchain.verify_queries as pbq
import puurrtybot.functions as pf
import puurrtybot.blockchain.verify_wallet as bvw
import puurrtybot.databases.database_functions as dff
import puurrtybot.twitter.verify_twitter as tvt
import puurrtybot.databases.get_functions as dgf

HIDDEN_STATUS = True

class TwitterVerifier(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.ctx_id = {}
        self.channel = self.client.get_channel(998321232208478219)

    async def static_loop(self, userid, twitter_handle, quantity, task_id, count):
        ctx = self.ctx_id[userid]
        check = tvt.verify_twitter(name=twitter_handle,  text = str(quantity), tweet_id='1549207713594343425')
        if check:
            await ctx.send(f"""<@{userid}>, reply found, your twitter account is now verified: {twitter_handle}""", hidden=HIDDEN_STATUS)
            dff.user_set_twitter(userid,twitter_handle)
            self._tasks[task_id][0].cancel()
        else:
            print(f"""not verified {userid} {twitter_handle}""")
            await ctx.send(f"""... still looking for reply. \n Next check for reply <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
            self.ctx_id[userid] = ctx

        self.counter[task_id] += 1
        if self.counter[task_id] > count:
            await ctx.send(f"""<@{userid}>, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')

    def task_launcher(self, userid, twitter_handle:str, quantity, seconds=5, count=5):
        new_task = tasks.loop(seconds=seconds, count = count)(self.static_loop)
        new_task.start(userid, twitter_handle, quantity, self.task_n, count)
        self._tasks[self.task_n] = (new_task, twitter_handle, quantity, self.task_n)
        self.counter[self.task_n] = 1
        self.task_n += 1
        

    @cog_ext.cog_slash(
        name = "verify_twitter",
        description = "verify_twitter",
        #guild_ids = [998321232208478219],
        options = [
        create_option(
                        name="twitter_handle",
                        description="twitter_handle",
                        required=True,
                        option_type=3)
                   ]
                      )
    async def verify_task(self, ctx:SlashContext, twitter_handle:str):
        userid = ctx.author_id
        twitter_handle = twitter_handle.strip('@')
        if dgf.user_get_twitter(userid) == twitter_handle:
            await ctx.send(f"""{ctx.author.mention}, {twitter_handle} already verified""", hidden=HIDDEN_STATUS)
        else:
            check = tvt.get_id_by_user(twitter_handle)
            if check:
                self.ctx_id[userid] = ctx
                quantity = str(int(float(pf.get_random_quantity())*1_000_000))+str(int(userid))
                await ctx.send(f"""**Verify a new twitter account** \n\n⌛ Please reply with **{quantity}** to https://twitter.com/PuurrtyBot/status/1549207713594343425 from **{twitter_handle}** within the next 60 minutes.""", hidden=HIDDEN_STATUS)
                self.task_launcher(userid, twitter_handle, quantity, seconds=60*5, count=12)
            else:
                await ctx.send(f"""{ctx.author.mention}, the entered twitter account **{twitter_handle}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)
        

    
def setup(client):
    client.add_cog(TwitterVerifier(client))
