import puurrtybot, asyncio, os, time, datetime
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("I am online")

@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)

bot.run(puurrtybot.DISCORD_TOKEN)