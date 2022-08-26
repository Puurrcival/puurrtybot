from venv import create
import puurrtybot, os, discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import puurrtybot.helper.functions as pf
import puurrtybot.assets.get_functions as agf
#import puurrtybot.users.user_updates as uup

import puurrtybot.database.query as dq
import puurrtybot.database.insert as di
from puurrtybot.helper import fuzzy_search, asset_profile

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    #pii.initialize_databases()
    puurrtybot.GUILD = bot.get_guild(puurrtybot.GUILD)
    for member in puurrtybot.GUILD.members:
        di.new_user(user_id = member.id, username = member.name)
    
    #    try:
    #        puurrtybot.USERS[str(member.id)]
    #    except KeyError:
    #        uup.new_user(str(member.id))
    #uup.user_all_update()
    print("I am online")


@bot.command()
async def update(ctx):
    await uup.user_update_roles_all(ctx.message.author.id)



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
async def search(ctx, *, text):
    try:
        match = pf.query_asset(f"""{text.strip()}""")
        #print(f"""https://{agf.get_asset_image_url(match[1])}""")
        sale_history = agf.get_asset_sale_history(match[1])
        #image = agf.get_asset_image(match[1], basewidth = 120)

        embed=discord.Embed(title=f"""**{match[0]}**""", url=f"""https://www.jpg.store/asset/{match[1]}""", description="", color=0x109319)

        # Add author, thumbnail, fields, and footer to the embed
        #embed.set_author(name="PuurrtyBot", url="https://infura-ipfs.io/ipfs/QmXdUjTyPEvPAnRk5Nc1TCje7JhLvrx1F45U3oS2YLWQ74")

        embed.set_thumbnail(url=f"""https://ipfs.io/ipfs/{agf.get_asset_image_url(match[1]).split('/')[-1]}""")

        embed.add_field(name=f"""Times traded""", value=f"""{sale_history['traded']}""", inline=False) 
        embed.add_field(name="Lowest", value=f"""{sale_history['lowest']} ₳""", inline=True)
        embed.add_field(name="Highest", value=f"""{sale_history['highest']} ₳""", inline=True)
        embed.add_field(name="Volume", value=f"""{sale_history['volume']} ₳""", inline=True)
        embed.add_field(name=f"""Minted""", value=f"""For {puurrtybot.ASSETS[match[1]]['mint_price']}₳ on {pf.timestamp_to_formatted_date_with_time(puurrtybot.ASSETS[match[1]]['mint_time'])}.""", inline=False)

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