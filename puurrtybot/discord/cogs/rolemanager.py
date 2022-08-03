from discord.ext import commands, tasks
import puurrtybot.roles.update_roles as rur


class RoleManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('RoleManager running')
        await rur.update_roles_n()
        await rur.update_roles_traits()


    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 60*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(RoleManager(client))