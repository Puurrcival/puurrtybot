from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import datetime
import puurrtybot.databases.get_functions as dgf
import puurrtybot.twitter.twitter_queries as ttq
import puurrtybot.twitterverifier.twitter_verify as tvt
import puurrtybot.users.user_updates as uuu
import puurrtybot

HIDDEN_STATUS = True

class TwitterVerifier(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}
        self.ctx_id = {}
        self.verification = {}
        self.channel = self.client.get_channel(998321232208478219)

    async def static_loop(self, userid, count):
        print('verify started')
        ctx = self.ctx_id[userid]
        check = self.verification[userid].verify_twitter()
        twitter_handle = self.verification[userid].twitter_account
        if check:
            await ctx.send(f"""<@{userid}>, reply found, your twitter account is now verified: {twitter_handle}""", hidden=HIDDEN_STATUS)
            puurrtybot.USERS[str(userid)]['twitter'] = twitter_handle
            uuu.save_user(str(userid))
            self._tasks[userid].cancel()
        else:
            print(f"""not verified {userid} {twitter_handle}""")
            await ctx.send(f"""... still looking for reply. \n Next check for reply <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
            self.ctx_id[userid] = ctx

        self.counter[userid] += 1
        if self.counter[userid] > count:
            await ctx.send(f"""<@{userid}>, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')

    def task_launcher(self, userid, seconds, count):
        new_task = tasks.loop(seconds = seconds, count = count)(self.static_loop)
        new_task.start(userid, count)
        self._tasks[userid] = new_task
        self.counter[userid] = 1
        

    @cog_ext.cog_slash(
        name = "verify_twitter",
        description = "verify_twitter",
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
        try:    
            self._tasks[userid].cancel()
        except KeyError:
            pass
        twitter_handle = twitter_handle.strip('@')
        twitter_id = ttq.get_id_by_user(twitter_handle)

        try:
            check = dgf.user_get_twitter(userid)
        except IndexError:
            check = False

        if check == twitter_handle:
            await ctx.send(f"""{ctx.author.mention}, {twitter_handle} already verified""", hidden=HIDDEN_STATUS)
        elif not twitter_id:
             await ctx.send(f"""{ctx.author.mention}, the entered twitter name **{twitter_handle}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)        
        else:
            self.verification[userid] = tvt.TwitterVerify(userid = userid, twitter_account = twitter_handle, twitter_id = twitter_id)
            self.ctx_id[userid] = ctx
            await ctx.send(f"""**Verify a new twitter account** \n\n⌛ Please reply with **{self.verification[userid].amount}** to https://twitter.com/PuurrtyBot/status/1549207713594343425 from **{twitter_handle}** within the next 60 minutes.""", hidden=HIDDEN_STATUS)
            self.task_launcher(userid, seconds=60*5, count=12)


def setup(client):
    client.add_cog(TwitterVerifier(client))