import discord
from discord import app_commands
from discord.ext import commands
GUILD_ID = 998148160243384321

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(test(bot), guilds = [discord.Object(id = GUILD_ID)])