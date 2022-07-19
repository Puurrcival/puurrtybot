import puurrtybot, asyncio, os, time, datetime, discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import puurrtybot.databases.database_functions as df
import puurrtybot.databases.get_functions as dgf
import puurrtybot.markets.market_queries as mmq

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    guild = bot.get_guild(998148160243384321)
    for member in guild.members:
        df.create_new_user(member.id)
    print("I am online")

@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)


@bot.command()
async def twitter(ctx):
    reply = dgf.user_get_twitter(ctx.message.author.id)
    await ctx.send(reply)


@bot.command()
async def cats_n(ctx):
    reply = dgf.user_get_assets_n(ctx.message.author.id)
    await ctx.send(reply)


@bot.command()
async def wallets(ctx):
    reply = dgf.user_get_stakes(ctx.message.author.id)
    if reply.strip()!='':
        await ctx.send(reply)
    else:
        await ctx.send("No verified wallet.")


for filename in os.listdir(puurrtybot.PATH/'puurrtybot/discord/cogs'):
    if filename.endswith('.py'):
        print(f"""cogs.{filename[:-3]}""")
        bot.load_extension(f"""cogs.{filename[:-3]}""")


bot.run(puurrtybot.DISCORD_TOKEN)