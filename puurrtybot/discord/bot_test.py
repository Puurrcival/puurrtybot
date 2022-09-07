import os

import discord
from discord import app_commands
from discord.ext import commands

import puurrtybot
from puurrtybot.helper import fuzzy_search, asset_profile
from puurrtybot.discord import button
from puurrtybot.discord.category.administration import registration
import puurrtybot.discord.embed as em

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
        self.inititial_extensions = []
        for root, _, files in os.walk(puurrtybot.PATH/'puurrtybot/discord/cogs'):
            for name in files:
                if name.endswith((".py")):
                    self.inititial_extensions.append(f"""cogs{root.split("/cogs")[-1]}/{name}""".replace("/",".")[:-3])

    async def setup_hook(self):
        for ext in self.inititial_extensions:
            print(ext)
            await self.load_extension(ext)

        await self.tree.sync(guild = discord.Object(id = GUILD_ID))
        self.add_view(button.button_verify_member())
        self.add_view(registration.ButtonVerify())

    async def on_ready(self):
        puurrtybot.GUILD = self.get_guild(puurrtybot.GUILD)
        puurrtybot.DISCORD_ROLES = {role.id:role for role in puurrtybot.GUILD.roles}
        print(f"Logged in as {self.user}.")

        member = puurrtybot.GUILD.get_member(642352900357750787)
        print(member)

    #async def on_command_error(self, ctx, error):
    #    await ctx.reply(error, ephemeral = True)
    

bot = Bot() 


@bot.hybrid_command(name = "create_button2", with_app_command = True, description = "Testing")
@app_commands.guilds(discord.Object(id = GUILD_ID))
@commands.has_permissions(administrator = True)
async def launch_button1(ctx: commands.Context): 
    await ctx.send(embed=em.VERIFY_EMBED, view = registration.ButtonVerify())


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