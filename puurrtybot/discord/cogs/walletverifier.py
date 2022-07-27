from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import datetime
import puurrtybot
import puurrtybot.walletverifier.wallet_verify as wwv
import puurrtybot.blockfrost.blockfrost_queries as bbq
import puurrtybot.users.user_updates as uuu


HIDDEN_STATUS = True

class WalletVerifier(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.counter = {}
        self.ctx_id = {}
        self.verification = {}
        self.channel = self.client.get_channel(998321232208478219)

    async def static_loop(self, userid, count):
        ctx = self.ctx_id[userid]
        check = self.verification[userid].verify_transaction()
        wallet = self.verification[userid]
        if check:
            await ctx.send(f"""<@{userid}>, transaction found, your address is now verified: {wallet}""", hidden=HIDDEN_STATUS)
            puurrtybot.USERS[str(user_id)]['addresses'] += [wallet]
            uuu.user_update(str(user_id))
            self._tasks[userid].cancel() 
        else:
            print(f"""not verified {userid} {wallet}""")
            await ctx.send(f"""... still looking for transaction. \n Next check for transaction <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
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
        name = "verify_wallet",
        description = "verify_wallet",
        options = [
            create_option(
                            name="wallet",
                            description="wallet address",
                            required=True,
                            option_type=3)
                   ]
                      )
    async def verify_task(self, ctx:SlashContext, wallet:str):
        userid = ctx.author_id
        try:    
            self._tasks[userid].cancel()
        except KeyError:
            pass
        address = wallet.strip()
        address = bbq.get_address_by_adahandle(address)

        if address in puurrtybot.USERS[str(user_id)]['addresses']:
            await ctx.send(f"""{ctx.author.mention}, you already verified this address: {address}""", hidden=HIDDEN_STATUS)
        elif not bbq.check_address_exists(address):
            await ctx.send(f"""{ctx.author.mention}, the entered address **{address}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)
        else:
            self.verification[userid] = wwv.WalletVerify(userid = userid, address = address)
            self.ctx_id[userid] = ctx

            amount = str(self.verification[userid].amount)
            amount_formatted = f"""{amount[:1]}.{amount[1:]}"""

            await ctx.send(f"""**Verify a new address** \n\n⌛ Please send **{amount_formatted}₳** to your own address at **{address}** within the next 60 minutes.\n\n⚠ Make sure to send from (and to) the wallet that owns this address. In case of error your fees will not be reimbursed by the operator of this Discord server.\n\n💡 If you close Discord, you can use /verify list to get your verification data later.""", hidden=HIDDEN_STATUS)
            self.task_launcher(userid, seconds=60*5, count=12)
    

def setup(client):
    client.add_cog(WalletVerifier(client))