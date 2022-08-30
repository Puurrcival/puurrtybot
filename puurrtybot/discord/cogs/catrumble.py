from dataclasses import dataclass
from typing import List
import random

import discord
from discord.ext import commands

import puurrtybot
from puurrtybot.database import query as dq, update as du
from puurrtybot.pcs import metadata as md


@dataclass(order=True)
class PartyUser:
    awake: bool = True
    rounds: int = 0
    won: int = 0
    n_cat: int = 0
    user_id: int = 0
    exhaust: int = 100
    balance: int = 0


    @property
    def mention(self):
        return f"""<@{self.user_id}>"""

    def __post_init__(self):
        self.n_cat = dq.get_asset_all_by_user_id(self.user_id)   


class CatRumble(commands.Cog):
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot

    async def static_loop(self):
        print('CatRumble running')
        channel = puurrtybot.GUILD.get_channel(1002178068451963030)
        init_msg = await channel.fetch_message(1008736955858690079)

        users = set()
        for reaction in init_msg.reactions:
            if reaction.emoji == """🎉""":
                async for user in reaction.users():
                    users.add(user.id)


        users: List[PartyUser] = [PartyUser(user_id = user_id) for user_id in users]

        embed1=discord.Embed(title=f"""Puurrty Time""", description=f"""Invited: {len(users)} \n Prize: 10.000 Coins \n Winning a round: 500 Coins""", color=0x109319)
        embed1.add_field(name=f"""Guest List""", value=f"{' '.join([user.mention for user in users])}", inline=False) 

        await channel.send(embed=embed1)

        traitsX = { 1: ('🐟 Fish Bobbling',     (md.Mask.DIVER, md.Hands.FISH_BOWL, md.Fur.SKELETON, md.Fur.CRYSTAL)),
                    2: ('🍗 Chicken Chomping ', (md.Hands.CHICKEN, md.Hands.KNIFE_AND_FORK, md.Hands.PIZZA, md.Hands.ONIGIRI, 
                                                 md.Hands.TAIYAKI, md.Outfit.LOBSTER_BIB, md.Outfit.CHEF, md.Mouth.DROOLING)),
                    3: ('🍺 Drinking Contest',  (md.Hands.BEER, md.Hands.MILK)),
                    4: ('🔥 Floor is Lava',     (md.Wings.ANGEL_WINGS, md.Eyes.FIRE_EYES, md.Hat.FIRE_BUCKET)),
                    5: ('🔫 Water Gun Fight',   (md.Hands.NERF_GUNS, md.Outfit.SCUBA_SUIT)),
                    6: ('🐶 Dodge the Dog',     (md.Mask.KITSUNE, md.Mask.JASON, md.Mask.CLOWN, md.Mouth.BEARD, md.Mouth.MUSTACHE)),
                    7: ('🐉 Dungeon and Cats',  (md.Hat.WIZARD_HAT, md.Outfit.WIZARD_ROBE, md.Hat.UNICRON_TIARA, md.Hands.WAND,
                                                 md.Hat.CROWN, md.Outfit.ROYAL_CLOAK, md.Hat.PHARAOH_HEADDRESS, md.Hat.PIRATE_HAT,
                                                 md.Outfit.PIRATE_JACKET)),
                    8: ('🕺🏽 Dance Contest',     (md.Hat.HEADPHONES, md.Outfit.HAWAIIAN, md.Outfit.HAWAIIAN_SHIRT)),
                    9: ('😬 Grimace',           (md.Mouth.DROOLING, md.Mouth.FANGS, md.Mouth.VERY_ANGRY, md.Mouth.NORMAL, 
                                                 md.Mouth.SMILING, md.Mouth.TONGUE_OUT, md.Mouth.HAPPY, md.Mouth.SERIOUS,
                                                 md.Mouth.ANGRY, md.Mouth.GROWLING)),
                   10: ('🎩 The Hat Game',      (md.Hat.BEANIE, md.Hat.STRAW_HAT, md.Hat.CAP, md.Hat.SOMBRERO, 
                                                 md.Hat.PARTY_HAT, md.Hat.CHEF_HAT)),
                   11: ('👀 Staring Contest',   (md.Eyes.HIDDEN, md.Eyes.SCAR_CRYSTAL_EYES, md.Eyes.STAR_GLASSES, md.Eyes.WHITE_EYES,
                                                 md.Eyes.SMALL_PUPILS, md.Eyes.CLOSED, md.Eyes.BLUE_AND_YELLOW, md.Eyes.GLOWING_YELLOW)),
                   12: ('📍 Hide and Seek',     (md.Outfit.HOODIE, md.Fur.DARK_GRAY_STRIPED, md.Fur.WHITE, md.Fur.BLACK, md.Fur.STRIPED, 
                                                 md.Fur.GRAY_STRIPED, md.Fur.BICOLOR, md.Fur.TRICOLOR, md.Fur.SIAMESE)),
                   13: ('😈 Truth or Dare',     (md.Hat.HALO, md.Hat.DEVIL, md.Outfit.NEKKID, md.Hands.SKATEBOARD)),
                   14: ('🪴 Licking Plants',    (md.Fur.CRYSTAL, md.Fur.PINK)),
                   15: ('🥷 Crazy 88',          (md.Outfit.SUIT, md.Hands.MACHETE))
                  }

        round = 0
        while traitsX:
            round += 1
            hit = random.choice(list(traitsX.keys()))
            game_name, traits = traitsX[hit]
            del traitsX[hit]

            traits_text = ', '.join([f"""{trait.class_name} {trait.value}""" for trait in traits])
            text = f"""Bonus: {traits_text} \n\n"""

            results = []
            for user in users:
                if user.awake:
                    n = dq.get_amount_of_assets_for_trait(traits, user.user_id)
                    roll = random.choice(range(1,101+n))
                    if roll < 51:
                        user.exhaust += -1*(10+int(roll/10))
                    else:
                        user.exhaust += -10
                    text += f"""<@{user.user_id}> <Bonus: {n} Cats> <event: {roll}> <exhaustion: {user.exhaust}> \n"""
                    results.append( (roll, user.user_id))
                    if user.exhaust < 1:
                        user.awake = False
                    else:
                        user.rounds += 1


            awake = sum([user.awake for user in users])
            print(f"""awake: {awake}""")
            if awake > 0:
                winner = sorted(results)[-1]
                user = [user for user in users if user.user_id == winner[1]][0]
                user.won += 1
                user.balance += 500
                text += f"""\n Round winner: <@{winner[1]}>\n"""
            else:
                text += f"""\n Round winner: No Winner.\n"""

            partyout = sum([not user.awake for user in users])
            text += f"""\n Cats Exhausted: {partyout}\n"""
            partyon = sum([user.awake for user in users])
            text += f"""\n Cats partying on: {partyon }\n"""
            embed2=discord.Embed(title=f"""__Round {round}: {game_name}__""", description=text, color=0x109319)

            await channel.send(embed=embed2)

            if awake < 2:
                break


        print("party ended")
        ranking = sorted([user for user in users], reverse=True)
        ranking[0].balance += 10_000
        text = f"""Winner of the Party: <@{ranking[0].user_id}> !!!\n\n"""
        for ix, user in enumerate(ranking):
            text += f"""{ix+1}. <@{user.user_id}> winning {user.balance} Coins.\n"""
            du.xxxxx(user.user_id, user.balance)
        embed2=discord.Embed(title=f"""__Party Ended__""", description=text, color=0x109319)  
        await channel.send(embed=embed2)


    @commands.Cog.listener()
    async def on_ready(self):
        #new_task = tasks.loop(seconds = 60*60, count = None)(self.static_loop)
        #new_task.start()
        pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CatRumble(bot), guilds = [discord.Object(id = 998148160243384321)])