import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import puurrtybot
import puurrtybot.database.query as dq
import puurrtybot.database.insert as di
from puurrtybot.helper import fuzzy_search, asset_profile

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    user_ids = [user.user_id for user in dq.get_user_all()]
    puurrtybot.GUILD = bot.get_guild(puurrtybot.GUILD)
    puurrtybot.DISCORD_ROLES = {role.id:role for role in puurrtybot.GUILD.roles}

    for member in puurrtybot.GUILD.members:
        if member.id not in user_ids:
            di.new_user(user_id = member.id, username = member.name)
    print("I am online")


@bot.command()
async def balance(ctx):
    await ctx.send(dq.get_user_by_user_id(ctx.message.author.id).balance)


@bot.command()
async def bal(ctx):
    await balance(ctx)


@bot.command()
async def party(ctx):
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
async def profile(ctx, *, text):
    for part in text.split(';'):
        match = fuzzy_search.query_asset(part.strip())
        if match:
            ap = asset_profile.AssetProfile(match[1])
            embed, embed_files = ap.embed
            await ctx.send(embed = embed, files = embed_files)
        else:
            await ctx.send(f"""Couldn't find a cat with that name.""")


@bot.command()
async def twitter(ctx):
    user = dq.get_user_by_user_id(ctx.message.author.id)
    if user.twitter_id:
        await ctx.send(f"""https://twitter.com/{user.twitter_handle}""")
    else:
        await ctx.send(f"""No verified twitter account found, use /verify_twitter to verify.""")


@bot.command()
async def n_cats(ctx):
    await ctx.send(dq.get_user_number_of_assets(ctx.message.author.id))


for filename in os.listdir(puurrtybot.PATH/'puurrtybot/discord/cogs'):
    if filename.endswith('.py'):
        print(f"""cogs.{filename[:-3]}""")
        bot.load_extension(f"""cogs.{filename[:-3]}""")


bot.run(puurrtybot.DISCORD_TOKEN)