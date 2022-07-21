from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import datetime
import puurrtybot.databases.database_functions as dff
import puurrtybot.walletverifier.wallet_verify as wwv
import puurrtybot.blockfrost.blockfrost_queries as bbq


HIDDEN_STATUS = True

class WalletVerifier(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
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
            dff.user_add_wallet(userid, wallet)
            dff.user_update_wallets(userid)
            dff.user_update_assets(userid)
            dff.user_update_traits(userid)
            self._tasks[userid][0].cancel()
        else:
            print(f"""not verified {userid} {wallet}""")
            await ctx.send(f"""... still looking for transaction. \n Next check for transaction <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
            self.ctx_id[userid] = ctx

        self.counter[userid] += 1
        if self.counter[userid] > count:
            await ctx.send(f"""<@{userid}>, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')

    def task_launcher(self, userid, wallet:str, amount, seconds=5, count=5):
        new_task = tasks.loop(seconds=seconds, count = count)(self.static_loop)
        new_task.start(userid, wallet, amount, count)
        self._tasks[userid] = (new_task, wallet, amount)
        self.counter[userid] = 1
        

    @cog_ext.cog_slash(
        name = "verify_wallet",
        description = "verify_wallet",
        #guild_ids = [998321232208478219],
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
        address = wallet.strip()
        address = bbq.get_address_by_adahandle(address)

        if dff.user_check_wallet_exists(userid, address):
            await ctx.send(f"""{ctx.author.mention}, you already verified this address: {address}""", hidden=HIDDEN_STATUS)
        elif not bbq.check_address_exists(address):
            await ctx.send(f"""{ctx.author.mention}, the entered address **{address}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)
        else:
            self.verification[userid] = wwv.WalletVerify(userid = userid, address = address)
            self.ctx_id[userid] = ctx

            amount = str(self.verification[userid].amount)
            amount_formatted = f"""{amount[:1]}.{amount[1:]}"""

            await ctx.send(f"""**Verify a new address** \n\n⌛ Please send **{amount_formatted}₳** to your own address at **{address}** within the next 60 minutes.\n\n⚠ Make sure to send from (and to) the wallet that owns this address. In case of error your fees will not be reimbursed by the operator of this Discord server.\n\n💡 If you close Discord, you can use /verify list to get your verification data later.""", hidden=HIDDEN_STATUS)
            self.task_launcher(userid, address, amount, seconds=60*5, count=12)
    
    #@tasks.loop(seconds=900) 
    #async def update_database(self):
    #    print('update database')
    #    pdq.verify_clean_outdated()
    #    dud.update_wallet_assets(user_id=str(642352900357750787) , address="addr1qyqggc5f3dgyx6ulwl4uqf8gucxvdahgpatjx27hutsusg79nee6glazchetycv3uewpraf7tfe60t3kud5l0cdkl5wqyj5xhy")
        
        
    #@commands.Cog.listener()
    #async def on_ready(self):
    #    await self.update_database.start()

def setup(client):
    client.add_cog(WalletVerifier(client))