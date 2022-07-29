from venv import create
import puurrtybot
import puurrtybot, os, discord, puurrtybot.initialize.initialize as pii
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import puurrtybot.users.get_functions as ugf
import puurrtybot.databases.get_functions as dgf
import puurrtybot.functions as pf
import puurrtybot.assets.get_functions as agf
import puurrtybot.users.user_updates as uup
import puurrtybot.roles.packs as prg
import time


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    #pii.initialize_databases()
    puurrtybot.GUILD = bot.get_guild(puurrtybot.GUILD)
    for member in puurrtybot.GUILD.members:
        try:
            puurrtybot.USERS[str(member.id)]
        except KeyError:
            uup.new_user(str(member.id))
    uup.user_all_update()
    print("I am online")


@bot.command()
async def ping(ctx):
    # Get the latency of the bot
    latency = bot.latency  # Included in the Discord.py library
    # Send it to the user
    await ctx.send(latency)


@bot.command()
async def roles(ctx):
    guild = puurrtybot.GUILD
    await ctx.send("\n".join([f"""{role.id}: {guild.get_role(role.id)}""" for role in guild.roles if role.id != 998148160243384321]))


@bot.command()
async def test(ctx):
    guild = bot.get_guild(998148160243384321)
    print(guild)
    member = guild.get_member(ctx.message.author.id)
    content = await prg.join_kitsune(guild, member.id)
    await ctx.send(content)


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
        embed.add_field(name=f"""Minted""", value=f"""For {puurrtybot.ASSETS[match[1]]['mint_price']}₳ on {pf.get_formatted_date(puurrtybot.ASSETS[match[1]]['mint_time'])}.""", inline=False)

        embed.set_footer(text="")
        if sale_history['traded']>1:
            image_stream = agf.get_asset_sale_history_plot(match[1])
            image_stream = discord.File(image_stream, filename="sales_plot.png")
            embed.add_field(name=f"""\u200b""", value=f"""**Sales History**""", inline=False) 
            embed.set_image(url="attachment://sales_plot.png")
            await ctx.send(embed=embed, file = image_stream)
        else:
            await ctx.send(embed=embed)
    except KeyError:
        await ctx.send(f"""Couldn't find a cat with that name.""")


@bot.command()
async def twitter(ctx):
    reply = puurrtybot.USERS[str(ctx.author.id)]['twitter']['handle']
    if reply:
        await ctx.send(f"""https://twitter.com/{reply}""")
    else:
        await ctx.send(f"""No verified twitter account found, use /verify_twitter to verify.""")


@bot.command()
async def n_cats(ctx):
    reply = ugf.user_get_n_cats(ctx.message.author.id)
    await ctx.send(reply)


@bot.command()
async def traits(ctx):
    reply = ugf.user_get_traits(ctx.message.author.id)
    await ctx.send(reply)


@bot.command()
async def wallets(ctx):
    reply = ugf.user_get_stakes(ctx.message.author.id)
    if reply.strip()!='':
        await ctx.send(reply)
    else:
        await ctx.send("No verified wallet.")


for filename in os.listdir(puurrtybot.PATH/'puurrtybot/discord/cogs'):
    if filename.endswith('.py'):
        print(f"""cogs.{filename[:-3]}""")
        bot.load_extension(f"""cogs.{filename[:-3]}""")


bot.run(puurrtybot.DISCORD_TOKEN)