import random
import datetime
import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from puurrtybot.api import blockfrostio
from puurrtybot.database import query as dq, insert as di
from puurrtybot.database.create import Address, User
from puurrtybot.discord.cogs.updatemanager import update_role_all_by_user


async def verify_transaction(address: str, past_time: int, amount: str, address_list: list = None):
    tx_hash_list = [tx_hash for tx_hash in blockfrostio.get_tx_hash_list_by_address(address, past_time=past_time)]
    utxo_list_list = [blockfrostio.get_utxo_list_by_tx_hash(tx_hash) for tx_hash in tx_hash_list]
    for utxo_list in utxo_list_list:
        if [True for utxo_input in utxo_list['inputs'] if utxo_input['address'] not in address_list]: return False
        for utxo_output in utxo_list['outputs']:
            if utxo_output['address'] == address and amount in [entry['quantity'] for entry in utxo_output['amount']]:
                return True
    return False


class WalletVerifier(commands.Cog):
    def __init__(self, client: commands.bot.Bot):
        self.client = client

    @app_commands.command(name = "verify_wallet", description = "Verify wallet.")
    async def verify_wallet(self, interaction: discord.Interaction, *, address: str):
        ctx: commands.Context = await commands.Context.from_interaction(interaction)
        adahandle = blockfrostio.get_address_by_adahandle(address)
        address: Address = Address( address = adahandle if adahandle else address, 
                                    user_id = interaction.user.id)
        amount = None
        if not blockfrostio.valid_address(address.address):
            content = f"""{interaction.user.mention}, the entered address <**{address.address}**> **doesn't exist**. Please check the spelling and try again."""
        elif dq.fetch_row(address):
            content = f"""{interaction.user.mention}, this address has been verified already: {address.address}"""
        else:
            amount = str(random.choice(list(range(2_000_000, 3_000_000+1))))
            content = f"""**Verify a new address** \n\n⌛ Please send **{amount}₳** to your own address at **{address.address}** within the next 60 minutes.\n\n⚠ Make sure to send from (and to) the wallet that owns this address. In case of error your fees will not be reimbursed by the operator of this Discord server.\n\n Will check every 3 minutes for transaction.\n\nNext check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>."""
        await interaction.response.send_message(content, ephemeral = True)

        if amount:
            time_window = 3*60
            await asyncio.sleep(time_window)
            message = await ctx.send(f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""", ephemeral=True)
            address_list = blockfrostio.get_address_list_by_stake_address(address.stake_address) if address.stake_address else []
            for _ in range(20):
                if await verify_transaction(address.address, time_window, amount, address_list) and not interaction.is_expired():
                    content = f"""<@{address.user_id}>, transaction found, your address is now verified: {address.address}"""
                    di.insert_row(address)
                    await ctx.send(content, ephemeral=True)
                    await update_role_all_by_user(dq.fetch_row(User(address.user_id)))     
                    break
                await asyncio.sleep(time_window)
                if not interaction.is_expired(): await message.edit(content = f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""")
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WalletVerifier(bot), guilds = [discord.Object(id = 998148160243384321)])