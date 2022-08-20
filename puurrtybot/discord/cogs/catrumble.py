from discord.ext import commands, tasks
import puurrtybot, discord, random
import puurrtybot.databases.database_queries as ddq

class CatRumble(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('CatRumble running')
        channel = puurrtybot.GUILD.get_channel(1002178068451963030)
        init_msg = await channel.fetch_message(1008736955858690079)
        users = set()
        for reaction in init_msg.reactions:

            users = set()
            if reaction.emoji == """🎉""":
                async for user in reaction.users():
                    users.add(user.id)
        #users_list = [f"""<@{user}>""" for user in users]
        users_list = [f"""<{user}>""" for user in users]

        embed1=discord.Embed(title=f"""Puurrty Time""", description=f"""Invited: {len(users)} \n Prize: 10.000 Coins \n Winning a round: 500 Coins""", color=0x109319)
        embed1.add_field(name=f"""Guest List""", value=f"{' '.join(users_list)}", inline=False) 

        #await channel.send(embed=embed1)

        ex = {user:100 for user in users}
        traitsX = {1: ('🐟 Fish Bobbling',      (('mask','Diver'),('hands','Fish Bowl'), ('fur', 'Skeleton'), ('fur','Crystal'))),
                  2: ('🍗 Chicken Chomping ',   (('hands','Chicken'),('hands','Fork and Knife'), ('hands', 'Pizza'), ('hands','Onigri'), ('hands','Taiyaki'), ('outfit','Lobster Bib'),('outfit','Chef'),('mouth', 'Drooling'))),
                  3: ('🍺 Drinking Contest',    (('hands','Beer'),('hands','Milk'))),
                  4: ('🔥 Floor is Lava',       (('wings','Wings'),('eyes','Fire Eyes'), ('hat', 'Fire Bucket'))),
                  5: ('🔫 Water Gun Fight',     (('hands','Nerf Guns'),('outfit','Scuba Suit'))),
                  6: ('🐶 Dodge the Dog',       (('mask','Kitsune'),('mask','Jason'),('mask','Clown'),('mouth','Beard'),('mouth','Mustache'))),
                  7: ('🐉 Dungeon and Cats',    (('hat','Wizard Hat'), ('outfit','Wizard Cloak'), ('hat','Unicorn Tiara'), ('hands', 'Wand'), ('hat','Crown'), ('outfit', 'Royal cloak'), ('hat', 'Pharaoh Headdress'), ('hat','Pirate Hat'), ('outfit','Pirate Jacket'))),
                  8: ('🕺🏽 Dance Contest',       (('hat','Headphones'), ('outfit','Hawaiian'), ('outfit','Hawaiian Shirt'))),
                  9: ('😬 Grimace',             (('mouth', 'Drooling'), ('mouth', 'Fangs'), ('mouth','Very Angry'), ('mouth','Normal'), ('mouth','Smiling'), ('mouth','Tongue out'), ('mouth','Happy'), ('mouth','Serious'), ('mouth','Angry'), ('mouth','Growling'))),
                  10: ('🎩 The Hat Game',       (('hat','Beanie'), ('hat','Straw Hat'), ('hat','Cap'), ('hat','Sombrero'), ('hat','Party Hat'), ('hat','Chef Hat'))),
                  11: ('👀 Staring Contest',    (('eyes','Hidden'), ('eyes','Scar crystal eye'), ('eyes','Star glasses'), ('eyes','White eyes'), ('eyes','Small pupils'), ('eyes','Closed'), ('eyes','Blue and yellow'), ('eyes','Glowing yellow')) ),
                  12: ('📍 Hide and Seek',      (('outfit','Hoodie'), ('fur','Dark gray striped'), ('fur','White'), ('fur','Black'), ('fur','Stripe'), ('fur','Gray striped'), ('fur','Bicolor'), ('fur','Tricolor'), ('fur','Siamese')) ),
                  13: ('😈 Truth or Dare',      (('hat','Halo'), ('hat','Devil'), ('tail','Devil Tail'), ('outfit','Nekkid'), ('hands','Skateboard'))),
                  14: ('🪴 Licking Plants',     (('fur','Crystal'), ('fur','Pink'))),
                  15: ('🥷 Crazy 88',           (('outfit','Suit'), ('hands','Machete')))
                  }

        round = 0
        while traitsX:
            round += 1
            hit = random.choice(list(traitsX.keys()))
            game_name, traits = traitsX[hit]
            del traitsX[hit]

            traits_text = ', '.join([f"""{k} {v}""" for (k,v) in traits])
            text = f"""Bonus: {traits_text} \n\n"""

            results = []
            for user in users:
                if ex[user]>0:
                    n = ddq.get_traits_role_qualify(traits, user)
                    roll = random.choice(range(1,101+n))
                    if roll < 51:
                        ex[user] += -1*(5+int(roll/10))
                    else:
                        ex[user] += -5
                    text += f"""<@{user}> <Bonus: {n} Cats> <event: {roll}> <exhaustion: {ex[user]}> \n"""
                    results.append( (roll, user))
            winner = sorted(results)[-1]
            text += f"""\n Round winner: <@{winner[1]}>\n"""
            partyout = len([x for x in ex.values() if x < 1])
            text += f"""\n Cats Exhausted: {partyout}\n"""
            partyon = len([x for x in ex.values() if x > 0])
            text += f"""\n Cats partying on: {partyon }\n"""

            embed2=discord.Embed(title=f"""__Round {round}: {game_name}__""", description=text, color=0x109319)
            #await channel.send(embed=embed2)


    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 60*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(CatRumble(client))