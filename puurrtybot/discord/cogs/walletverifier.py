import random, datetime

from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option

from puurrtybot.helper import functions as hf
from puurrtybot.api import blockfrost
from puurrtybot.database import query as dq, insert as di
from puurrtybot.discord.cogs.updatemanager import update_role_all_by_user

HIDDEN_STATUS = True


class WalletVerify:
    def __init__(self, userid: int, address: str = None):
        self.address = address
        self.userid = userid
        self.stake_address = blockfrost.get_stake_address_by_address(self.address)
        self.address_list = blockfrost.get_address_list_by_stake_address(self.stake_address)
        self.amount = str(random.choice(list(range(2_000_000, 3_000_000+1))))
        self.time = hf.get_utc_time()

    def verify_transaction(self):
        self.tx_hash_list = blockfrost.get_tx_hash_list_by_address(self.address)
        for tx_hash in self.tx_hash_list:
            utxo_list = blockfrost.get_utxo_list_by_tx_hash(tx_hash)
            utxo_list = blockfrost.get_utxo_list_by_tx_hash(tx_hash)
            for utxo_input in utxo_list['inputs']:
                if utxo_input['address'] not in self.address_list:
                    return False
            for utxo_output in utxo_list['outputs']:
                if utxo_output['address'] == self.address and self.amount in [entry['quantity'] for entry in utxo_output['amount']]:
                    return True
        return False


class WalletVerifier(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client
        self._tasks = {} 
        self.counter = {}
        self.ctx_id = {}
        self.verification = {}


    async def static_loop(self, userid: int, count: int):
        ctx = self.ctx_id[userid]
        check = self.verification[userid].verify_transaction()
        wallet = self.verification[userid].address
        if check:
            print(f"""verified {userid} {wallet}""")
            await ctx.send(f"""<@{userid}>, transaction found, your address is now verified: {wallet}""", hidden=HIDDEN_STATUS)
            di.new_address(address = wallet, user_id = userid)
            await update_role_all_by_user(dq.get_user_by_user_id(userid))
            self._tasks[userid].cancel()
        else:
            print(f"""not verified {userid} {wallet}""")
            await ctx.send(f"""... still looking for transaction. \n Next check for transaction <t:{int(datetime.datetime.now().timestamp())+60*5}:R>.""", hidden=HIDDEN_STATUS)
            self.ctx_id[userid] = ctx

        self.counter[userid] += 1
        if self.counter[userid] > count:
            await ctx.send(f"""<@{userid}>, verifying time exceeded.""", hidden=HIDDEN_STATUS)
            print('time exceeded')

    def task_launcher(self, userid: int, seconds: int, count: int):
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
    async def verify_task(self, ctx: SlashContext, wallet: str):
        print(wallet)
        userid = ctx.author_id
        try:    
            self._tasks[userid].cancel()
        except KeyError:
            pass
        address = wallet.strip()
        address = blockfrost.get_address_by_adahandle(address)

        if dq.get_address_by_address(address):
            await ctx.send(f"""{ctx.author.mention}, this address has been verified already: {address}""", hidden=HIDDEN_STATUS)
        elif not blockfrost.valid_address(address):
            await ctx.send(f"""{ctx.author.mention}, the entered address **{address}** **doesn't exist**. Please check the spelling and try again.""", hidden=HIDDEN_STATUS)
        else:
            self.verification[userid] = WalletVerify(userid = userid, address = address)
            self.ctx_id[userid] = ctx

            amount = str(self.verification[userid].amount)
            amount_formatted = f"""{amount[:1]}.{amount[1:]}"""

            await ctx.send(f"""**Verify a new address** \n\n⌛ Please send **{amount_formatted}₳** to your own address at **{address}** within the next 60 minutes.\n\n⚠ Make sure to send from (and to) the wallet that owns this address. In case of error your fees will not be reimbursed by the operator of this Discord server.\n\n💡 If you close Discord, you can use /verify list to get your verification data later.""", hidden=HIDDEN_STATUS)
            self.task_launcher(userid, seconds=60*5, count=12)
    

def setup(client: commands.bot.Bot):
    client.add_cog(WalletVerifier(client))