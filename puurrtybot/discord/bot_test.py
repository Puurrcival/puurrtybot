import os

import discord
from discord import app_commands
from discord.ext import commands

import puurrtybot
from puurrtybot.helper import fuzzy_search, asset_profile
from puurrtybot.discord import button
from puurrtybot.discord.embed import RULES_EMBED

GUILD_ID = 998148160243384321
ROLE_ID = 1003995806434603059


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.message_content = True
        super().__init__(command_prefix = "!", intents = intents)
        self.inititial_extensions = [f"""cogs.{filename[:-3]}""" for filename in os.listdir(puurrtybot.PATH/'puurrtybot/discord/cogs') if filename.endswith('.py')]


    async def setup_hook(self):
        for ext in self.inititial_extensions:
            print(ext)
            await self.load_extension(ext)

        await self.tree.sync(guild = discord.Object(id = GUILD_ID))
        self.add_view(button.button_verify_member())
        self.add_view(button.button_verify())

    async def on_ready(self):
        puurrtybot.GUILD = self.get_guild(puurrtybot.GUILD)
        puurrtybot.DISCORD_ROLES = {role.id:role for role in puurrtybot.GUILD.roles}
        print(f"Logged in as {self.user}.")

    #async def on_command_error(self, ctx, error):
    #    await ctx.reply(error, ephemeral = True)
    

bot = Bot() 


@bot.hybrid_command(name = "create_button", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = GUILD_ID))
@commands.has_permissions(administrator = True)
async def launch_button1(ctx: commands.Context): 
    await ctx.send(embed=RULES_EMBED, view = button.button_verify_member())


@bot.tree.command(name = "profile", description = "Get information of a cat.")
@app_commands.guilds(discord.Object(id = GUILD_ID))
async def profile(interaction: discord.Interaction, *, text: str):
    for part in text.split(';'):
        match = fuzzy_search.query_asset(part.strip())
        if match:
            ap = asset_profile.AssetProfile(match[1])
            embed, embed_files = ap.embed
            await interaction.response.send_message(embed = embed, files = embed_files, ephemeral=True)
        else:
            await interaction.response.send_message(f"""Couldn't find a cat with that name.""", ephemeral=True)


bot.run(puurrtybot.DISCORD_TOKEN)