import random
import datetime
import asyncio
from typing import Tuple, Optional

import discord
from discord.ext import commands

from puurrtybot.api import jpgstore, blockfrostio
from puurrtybot.database import query as dq, update as du, insert as di
from puurrtybot.database.create import User, Asset, Address
import puurrtybot.api.twitter as twitter



async def verify_jpgstore(interaction: discord.Interaction):
        user = interaction.user
        hash_key = f"""pcs{random.getrandbits(128)}"""
        accounts = list(set([asset.address for asset in dq.fetch_row_by_value(Asset, Asset().column.discord_handle, interaction.user.name, all = True)]))
        accounts = [f"""**{jpgstore.get_jpgstore_profile_by_address(account).get('username')}**""" for account in accounts]
        content = ""
        if dq.fetch_row_by_value(Asset, Asset().column.discord_handle, str(user)):
            content = f"""You already verified the following accounts from jpgstore:\n{'; '.join(accounts)}\n\nIf you like to add another go ahead."""
        embed=discord.Embed(title="Puurrty Cats Society jpg.store Verification", color=0xed1212)
        embed.add_field(name="⌛ You have 15 minutes to change your jpg.store username to:", value=f"{hash_key}", inline=False)
        await interaction.followup.send(content=content, embed=embed, ephemeral = True)

        time_window = 3*60    
        message = await interaction.followup.send(f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""", ephemeral=True)
        for _ in range(5):
            response = jpgstore.get_jpgstore_profile_by_address(hash_key)
            if response.get('username') == hash_key:
                stake_address = response.get('stake_key')
                new_addresses = blockfrostio.get_address_list_by_stake_address(stake_address)
                for address in new_addresses:
                    new_address = Address(address, stake_address, user.id)
                    if not dq.fetch_row(new_address): di.insert_row(new_address)
                if not interaction.is_expired(): await message.edit(content = f"""Verification of **{response.get('stake_key')}** successful.""") 
                break
            await asyncio.sleep(time_window)
            if not interaction.is_expired(): await message.edit(content = f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""")

async def verify_twitter_check(hash_key: int) -> Optional[Tuple[int,str]]:
    response: list = twitter.get_conversation_by_conversation_id('1549207713594343425')
    tweets, users = response.get('data', ()), response.get('includes', {}).get('users')
    author_id = {0:tweet.get('author_id') for tweet in tweets if str(hash_key) in tweet.get('text', '')}.get(0)
    twitter_handle = {0:user.get('username') for user in users if str(user.get('id')) == author_id}.get(0)
    if author_id: return (int(author_id), twitter_handle)
    else: return (None, None)

async def verify_twitter(interaction: discord.Interaction):
        user: User = dq.fetch_row(User(interaction.user.id))
        hash_key = random.getrandbits(128)
        if user.twitter_handle:
            content = f"""You already verified the twitter account **{user.twitter_handle}**, if you verify a new account, it will be replaced."""
        else:
            content = f""""""
        embed=discord.Embed(title="Twitter Verification Message", url="https://twitter.com/PuurrtyBot/status/1549207713594343425", color=0xed1212)
        embed.add_field(name="⌛ You have 15 minutes to click the link and reply with:", value=f"{hash_key}", inline=False)
        await interaction.response.send_message(content=content, embed=embed, ephemeral = True)

        time_window = 3*60    
        message = await interaction.followup.send(f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""", ephemeral=True)
        for _ in range(5):
            user.twitter_id, user.twitter_handle = await verify_twitter_check(hash_key)
            if user.twitter_id:
                du.update_object(user)
                if not interaction.is_expired(): await message.edit(content = f"""Verification of **{user.twitter_handle}** successful.""") 
                break
            await asyncio.sleep(time_window)
            if not interaction.is_expired(): await message.edit(content = f"""Next check: <t:{int(datetime.datetime.now().timestamp())+time_window}:R>.""")

class ButtonVerifyWallet(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown_blockchain = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.cooldown_jpgstore = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @discord.ui.button(label = "Blockchain", style = discord.ButtonStyle.green, custom_id = "verify_blockchain_button", emoji="<:Coin:1004013428324696094>")
    async def verify_blockchain(self, interaction: discord.Interaction, button: discord.ui.Button):
        bucket = self.cooldown_blockchain.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.followup.send(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            await interaction.followup.send(f"""Verify Blockhain <Trigger Event>.""", ephemeral=True)

    @discord.ui.button(label = "JPG Store", style = discord.ButtonStyle.green, custom_id = "verify_jpgstore_button", emoji="<:jpgstore:1014929669839126608>")
    async def verify_jpgstore(self, interaction: discord.Interaction, button: discord.ui.Button):
        bucket = self.cooldown_jpgstore.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.followup.send(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            await verify_jpgstore(interaction)


class ModalWallet(discord.ui.Modal, title="Placeholder"):
    answer = discord.ui.TextInput(label = "Enter your Cardano address or ada handle", style=discord.TextStyle.short, placeholder="addr1.../$handle", default="nothing", required=True, max_length=150)
    interaction = None

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.interaction = interaction
        await interaction.response.defer()


class ButtonVerify(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown_wallet = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.cooldown_twitter = commands.CooldownMapping.from_cooldown(1, 5*60, commands.BucketType.member)
        self.cooldown_poker = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @discord.ui.button(label = "Register Wallet", style = discord.ButtonStyle.green, custom_id = "verify_wallet_button", emoji="👛")
    async def verify_wallet(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_wallet.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
           await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            wallet_modal = ModalWallet()
            await interaction.response.send_modal(wallet_modal)
            await wallet_modal.wait()
            await wallet_modal.interaction.followup.send(view=ButtonVerifyWallet(), ephemeral=True)

    @discord.ui.button(label = "Register Twitter", style = discord.ButtonStyle.green, custom_id = "verify_twitter_button", emoji="🐦")
    async def verify_twitter(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_twitter.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            await verify_twitter(interaction)

    @discord.ui.button(label = "Register Poker", style = discord.ButtonStyle.green, custom_id = "verify_poker_button", emoji="<:poker_chip:1014635979816050799>")
    async def verify_poker(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_poker.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            await interaction.response.send_message(f"""Verify Poker <Placeholder>.""", ephemeral=True)

