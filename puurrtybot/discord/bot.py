import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import puurrtybot
from puurrtybot.database.create import User
from puurrtybot.database import query as dq, insert as di
from puurrtybot.helper import fuzzy_search, asset_profile, image_handle

intents = discord.Intents.default()
intents.members = True


bot: commands.Bot = commands.Bot(command_prefix='!', intents=intents)
slash: SlashCommand = SlashCommand(bot, sync_commands=True)

from puurrtybot.data.text import RULES_EMBED


class StandardButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Klicke mich!",
            style=discord.enums.ButtonStyle.blurple,
            custom_id="interaction:DefaultButton"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Yeyy!.", ephemeral=True)
        
@bot.command()
async def hallo(ctx):
    #view = discord.ui.View(timeout=None)
    #view.add_item(StandardButton())
    await ctx.send(f"Hallo {ctx.author.mention}!")


@bot.command()
async def hallo2(ctx):
    view = discord.ui.View(timeout=None)
    view.add_item(StandardButton())
    await ctx.send(f"Hallo {ctx.author.mention}!")

'''
@bot.command()
async def rules(ctx):
    message = await ctx.send(embed=RULES_EMBED)
    await message.add_reaction('🔎')



@bot.event
async def on_ready() -> None:
    """On bot start do stuff."""
    user_ids = [user.user_id for user in dq.fetch_table(User)]
    puurrtybot.GUILD = bot.get_guild(puurrtybot.GUILD)
    puurrtybot.DISCORD_ROLES = {role.id:role for role in puurrtybot.GUILD.roles}

    for member in puurrtybot.GUILD.members:
        if member.id not in user_ids:
            di.insert_row(User(user_id = member.id, username = member.name))
    print("I am online")


#@bot.event
#async def on_message(message): 
#    if message.channel.id == 998321232208478219:
#        await message.channel.purge(limit=1)



@bot.command()
async def balance(ctx: commands.Context) -> None:
    """Reply with balance of an user."""
    await ctx.send(dq.fetch_row(User(ctx.message.author.id)).balance)


@bot.command()
async def bal(ctx: commands.Context):
    await balance(ctx)


@bot.command()
async def party(ctx: commands.Context):
    if ctx.message.author.id == 642352900357750787:
        await ctx.send("""A party is about to start join with :tada:""")

#@bot.command()
#async def addbalance(ctx):
#    ddi.user_add_balance(ctx.message.author.id, 10)


#@bot.command()
#async def test(ctx):
#    user_id = str(ctx.message.author.id)
#    count = 0
#    for asset in puurrtybot.USERS[user_id]['assets']:
#        try:
#           puurrtybot.ASSETS_SALES_HISTORY[asset]
#       except KeyError:
#           count += 1
#   await ctx.send(f"""You hold {count} minted diamond cats.""")

@bot.command()
async def puurrdo(ctx: commands.Context):
    image, answer = image_handle.puurrdo()
    embed = discord.Embed(  title=f"""**Where is Puurrdo?**""",
                            color=0x109319)

    image_file = discord.File(image, filename="puurrdo.png")
    embed.set_image(url=f"""attachment://puurrdo.png""")
    await ctx.send(embed = embed, file = image_file)


@bot.command()
async def profile(ctx: commands.Context, *, text: str):
    for part in text.split(';'):
        match = fuzzy_search.query_asset(part.strip())
        if match:
            ap = asset_profile.AssetProfile(match[1])
            embed, embed_files = ap.embed
            await ctx.send(embed = embed, files = embed_files)
        else:
            await ctx.send(f"""Couldn't find a cat with that name.""")


@bot.command()
async def twitter(ctx: commands.Context):
    user = dq.fetch_row(User(ctx.message.author.id))
    if user.twitter_id:
        await ctx.send(f"""https://twitter.com/{user.twitter_handle}""")
    else:
        await ctx.send(f"""No verified twitter account found, use /verify_twitter to verify.""")


@bot.command()
async def n_cats(ctx: commands.Context):
    await ctx.send(dq.get_asset_all_by_user_id(ctx.message.author.id))


for filename in os.listdir(puurrtybot.PATH/'puurrtybot/discord/cogs'):
    if filename.endswith('.py'):
        print(f"""cogs.{filename[:-3]}""")
        bot.load_extension(f"""cogs.{filename[:-3]}""")

'''
bot.run(puurrtybot.DISCORD_TOKEN)