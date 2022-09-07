import discord
from discord.ext import commands

import puurrtybot
from puurrtybot.database.create import User
from puurrtybot.pcs.role import Status
from puurrtybot.database import query as dq
from puurrtybot.discord.cogs.memberverifier import find_puurrdo
from puurrtybot.discord.category.welcome import cat_door
from puurrtybot.discord import modal


class button_verify_member(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown_verify = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.cooldown_tour = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @discord.ui.button(label = "Find Puurrdo", style = discord.ButtonStyle.green, custom_id = "verify_member_button", emoji="🔎")
    async def verify_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        interaction.message.author = interaction.user
        bucket = self.cooldown_verify.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            await interaction.followup.send(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        elif dq.fetch_row(User(interaction.user.id)):
            await interaction.user.add_roles(puurrtybot.DISCORD_ROLES[Status.VERIFIED.value.role_id])
            await interaction.followup.send("""You are already verified.""", ephemeral=True)
        else:
            await find_puurrdo(interaction)

    @discord.ui.button(label = "Take a tour", style = discord.ButtonStyle.green, custom_id = "verify_tour_button", emoji="🌆")
    async def verify_tour(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_tour.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        elif not dq.fetch_row(User(interaction.user.id)):
            await interaction.response.send_message("""You must find Puurrdo first.""", ephemeral=True)
        else:
            await interaction.response.send_message("""<Placeholder: trigger event tour.>""", ephemeral=True)


# class button_verify_wallet(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#         self.cooldown_blockchain = commands.CooldownMapping.from_cooldown(1, 5*60, commands.BucketType.member)
#         self.cooldown_jpgstore = commands.CooldownMapping.from_cooldown(1, 5*60, commands.BucketType.member)

#     @discord.ui.button(label = "Blockchain", style = discord.ButtonStyle.green, custom_id = "verify_blockchain_button", emoji="<:Coin:1004013428324696094>")
#     async def verify_blockchain(self, interaction: discord.Interaction, button: discord.ui.Button):
#         #await interaction.response.send_modal(modal.WalletModal())
#         #await interaction.response.defer()
#         bucket = self.cooldown_blockchain.get_bucket(interaction.message)
#         retry = bucket.update_rate_limit()
#         #if retry:
#         #    await interaction.followup.send(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
#         #else:
#         #    await interaction.response.send_modal(modal.WalletModal())
#             #await interaction.followup.send_m(f"""Verify Blockhain <Placeholder>.""", ephemeral=True)

#     @discord.ui.button(label = "JPG Store", style = discord.ButtonStyle.green, custom_id = "verify_jpgstore_button", emoji="<:jpgstore:1014929669839126608>")
#     async def verify_jpgstore(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.defer()
#         bucket = self.cooldown_jpgstore.get_bucket(interaction.message)
#         retry = bucket.update_rate_limit()
#         if retry:
#             await interaction.followup.send(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
#         else:
#             await verify.verify_jpgstore(interaction)


# class button_verify(discord.ui.View):
#     def __init__(self) -> None:
#         super().__init__(timeout=None)
#         self.cooldown_wallet = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
#         self.cooldown_twitter = commands.CooldownMapping.from_cooldown(1, 5*60, commands.BucketType.member)
#         self.cooldown_poker = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

#     @discord.ui.button(label = "Register Wallet", style = discord.ButtonStyle.green, custom_id = "verify_wallet_button", emoji="👛")
#     async def verify_wallet(self, interaction: discord.Interaction, button: discord.ui.Button):
#         addr = await interaction.response.send_modal(modal.WalletModal())
#         #await interaction.followup.send(f"""{addr}""", ephemeral=True)
#         #interaction.message.author = interaction.user
#         #bucket = self.cooldown_wallet.get_bucket(interaction.message)
#         #retry = bucket.update_rate_limit()
#         #if retry:
#         #    await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
#         #else:
#         #    print('x')
#         #    await interaction.response.send_message(view = button_verify_wallet(), ephemeral=True)

#     @discord.ui.button(label = "Register Twitter", style = discord.ButtonStyle.green, custom_id = "verify_twitter_button", emoji="🐦")
#     async def verify_twitter(self, interaction: discord.Interaction, button: discord.ui.Button):
#         interaction.message.author = interaction.user
#         bucket = self.cooldown_twitter.get_bucket(interaction.message)
#         retry = bucket.update_rate_limit()
#         if retry:
#             await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
#         else:
#             await verify.verify_twitter(interaction)

#     @discord.ui.button(label = "Register Poker", style = discord.ButtonStyle.green, custom_id = "verify_poker_button", emoji="<:poker_chip:1014635979816050799>")
#     async def verify_poker(self, interaction: discord.Interaction, button: discord.ui.Button):
#         interaction.message.author = interaction.user
#         bucket = self.cooldown_poker.get_bucket(interaction.message)
#         retry = bucket.update_rate_limit()
#         if retry:
#             await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
#         else:
#             await interaction.response.send_message(f"""Verify Poker <Placeholder>.""", ephemeral=True)