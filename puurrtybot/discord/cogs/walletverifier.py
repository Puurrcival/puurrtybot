from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import random, datetime
import puurrtybot.blockchain.verify_queries as pbq
import puurrtybot.functions as pf
import puurrtybot.blockchain.verify_wallet as bvw
import puurrtybot.databases.database_functions as dff

HIDDEN_STATUS = True

class WalletVerifier(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._tasks = {} 
        self.task_n = 0
        self.counter = {}

    async def static_loop(self, ctx, wallet, quantity, task_id, count):
        userid = ctx.author.id
        check = bvw.verify_wallet(address=wallet, quantity=quantity)
        if check:
            await ctx.send(f"""{ctx.author.mention}, transaction found, your address is now verified: {wallet}""", hidden=HIDDEN_STATUS)
            dff.user_add_wallet(userid, wallet)
            dff.user_update_wallets(userid)
            dff.user_update_assets(userid)
            self._tasks[task_id][0].cancel()
        else:
            print(f"""not verified {userid} {wallet}""")
            await ctx.send(f"""... still looking for transaction.""", hidden=HIDDEN_STATUS)

        self.counter[task_id] += 1
        if self.counter[task_id] > count:
            await ctx.send(f"""{ctx.author.mention}, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')

    def task_launcher(self, ctx, wallet:str, quantity, seconds=5, count=5):
        new_task = tasks.loop(seconds=seconds, count = count)(self.static_loop)
        new_task.start(ctx, wallet, quantity, self.task_n, count)
        self._tasks[self.task_n] = (new_task, wallet, quantity, self.task_n)
        self.counter[self.task_n] = 1
        self.task_n += 1
        

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
        quantity = pf.get_random_quantity()
        #wallet_check = pbq.get_address_by_adahandle(wallet)
        #pbq.verify_wallet_stats(ctx.author.id, wallet_check, quantity)
        wallet_check = bvw.get_address_by_adahandle(address=wallet)
        if wallet_check:
            check = dff.user_check_wallet_exists(ctx.author_id, wallet)
            if not check:
                await ctx.send(f"""{ctx.author.mention}, the address is verified: {wallet}""", hidden=HIDDEN_STATUS)
                return None

            await ctx.send(f"""**Verify a new address** \n\n
    ⌛ Please send **{quantity}₳** to your own address at **{wallet_check}** within the next 60 minutes.

    ⚠ Do not include any other tokens and make sure to send from (and to) the wallet that owns this address. Transactions that include outputs to any other addresses will not be considered and your fees will not be reimbursed by the operator of this Discord server.

    💡 If you close Discord, you can use /verify list to get your verification data later.""", hidden=HIDDEN_STATUS)
            self.task_launcher(ctx, wallet_check, quantity, seconds=60*5, count=12)
            await ctx.send(f'{ctx.author.mention} you started a wallet verification! \n Next check for transaction in <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.', hidden=HIDDEN_STATUS)
        else:
            await ctx.send(f"""{ctx.author.mention}, the entered wallet **{wallet}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)
        
    
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