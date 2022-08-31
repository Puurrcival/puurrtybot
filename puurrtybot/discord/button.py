import discord
from discord.ext import commands

import puurrtybot
from puurrtybot.database.create import User
from puurrtybot.pcs.role import Status
from puurrtybot.database import query as dq
from puurrtybot.discord.cogs.memberverifier import find_puurrdo

class button_verify_member(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown_verify = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.cooldown_tour = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @discord.ui.button(label = "Find Puurrdo", style = discord.ButtonStyle.green, custom_id = "verify_member_button", emoji="🔎")
    async def verify_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_verify.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        elif dq.fetch_row(User(interaction.user.id)):
            await interaction.user.add_roles(puurrtybot.DISCORD_ROLES[Status.VERIFIED.value.role_id])
            await interaction.response.send_message("""You are already verified.""", ephemeral=True)
        else:
            return await find_puurrdo(interaction)

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


class button_verify(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown_wallet = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
        self.cooldown_twitter = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)

    @discord.ui.button(label = "verify_wallet", style = discord.ButtonStyle.green, custom_id = "verify_wallet_button", emoji="<:Coin:1004013428324696094>")
    async def verify_wallet(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_wallet.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            return await interaction.response.send_message(f"""Verify Wallet <Placeholder>.""", ephemeral=True)

    @discord.ui.button(label = "verify_twitter", style = discord.ButtonStyle.green, custom_id = "verify_twitter_button", emoji="🐦")
    async def verify_twitter(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown_twitter.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            return await interaction.response.send_message(f"""Verify Twitter <Placeholder>.""", ephemeral=True)