from discord.ext import commands, tasks
import puurrtybot.users.user_updates as uuu
import puurrtybot

class RoleManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('RoleManager running')
        for member in puurrtybot.GUILD.members:
            pass#await uuu.user_update_roles_all(member.id)


    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 60*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(RoleManager(client))