import discord
from discord import app_commands
from discord.ext import commands

from puurrtybot.database import query
from puurrtybot.pcs.role import Family

FAMILY_DICT = {e.name.title():e.value.role_id for e in Family}


class FamilyManager(commands.Cog):
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot

    @app_commands.command(name = "join_family", description = "Join a family.")
    @app_commands.describe(family_name = "Family name")
    @app_commands.choices(family_name = [app_commands.Choice(name = name, value = str(value)) for name, value in FAMILY_DICT.items()])
    async def join_pack(self, interaction: discord.Interaction, family_name: app_commands.Choice[str]) -> None:
        new_role = interaction.guild.get_role(int(family_name.value))
        old_role = {0:role for role in interaction.user.roles if role.id in FAMILY_DICT.values()}.get(0, None)
        if old_role and old_role.id == new_role.id:
            content = f"""{interaction.user.mention} you are already in {new_role.mention}."""
        elif query.check_role_requirement(new_role.id, interaction.user.id):    
            leave_role = " "
            if old_role:
                await interaction.user.remove_roles(old_role)
                leave_role = f""" have left {old_role.mention} and"""
            content = f"""{interaction.user.mention} you{leave_role} joined {new_role.mention}."""
            await interaction.user.add_roles(new_role)
        else:
            requirement = '; '.join([str(e) for e in getattr(Family, 'ANGEL').value.requirement])
            content = f"""{interaction.user.mention} can't join {new_role.mention} missing <{requirement}>."""
        await interaction.response.send_message(content, ephemeral=True)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FamilyManager(bot), guilds = [discord.Object(id = 998148160243384321)])