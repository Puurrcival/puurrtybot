from discord.ext import commands, tasks
import puurrtybot
import puurrtybot.roles.update_roles as rur

class RoleManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('RoleManager running')
        #update role function
        guild = self.client.get_guild(998148160243384321)
        for user_id in puurrtybot.USERS.keys():
            await rur.update_roles_n(guild, user_id)


        

    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 5*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(RoleManager(client))