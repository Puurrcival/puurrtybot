import puurrtybot, os, discord, datetime
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import puurrtybot.databases.database_functions as df
import puurrtybot.databases.get_functions as dgf
import puurrtybot.functions as pf
import puurrtybot.assets.get_functions as agf

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
async def search(ctx, *, text):
    try:
        match = pf.query_asset(f"""{text}""")
        #print(f"""https://{agf.get_asset_image_url(match[1])}""")
        sale_history = agf.get_asset_sale_history(match[1])
        #image = agf.get_asset_image(match[1], basewidth = 120)

        embed=discord.Embed(title=f"""**{match[0]}**""", url=f"""https://www.jpg.store/asset/{match[1]}""", description="", color=0x109319)

        # Add author, thumbnail, fields, and footer to the embed
        #embed.set_author(name="PuurrtyBot", url="https://infura-ipfs.io/ipfs/QmXdUjTyPEvPAnRk5Nc1TCje7JhLvrx1F45U3oS2YLWQ74")

        embed.set_thumbnail(url=f"""https://infura-ipfs.io/ipfs/{agf.get_asset_image_url(match[1]).split('/')[-1]}""")

        embed.add_field(name=f"""Times traded""", value=f"""{sale_history['traded']}""", inline=False) 
        embed.add_field(name="Lowest", value=f"""{sale_history['lowest']} ₳""", inline=True)
        embed.add_field(name="Highest", value=f"""{sale_history['highest']} ₳""", inline=True)
        embed.add_field(name="Volume", value=f"""{sale_history['volume']} ₳""", inline=True)
        embed.add_field(name=f"""Minted""", value=f"""For {puurrtybot.ASSETS[match[1]]['mint_price']}₳ at {pf.timestamp_to_utctime(puurrtybot.ASSETS[match[1]]['mint_time'])} UTC.""", inline=False)

        embed.set_footer(text="")
        #await ctx.send(content = f"""{match}\n{sale_history}""", file=discord.File(fp=image, filename='cat.png'))
        await ctx.send(embed=embed)
    except KeyError:
        await ctx.send(f"""Couldn't find a cat with that name.""")


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