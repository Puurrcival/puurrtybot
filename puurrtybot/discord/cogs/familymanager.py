from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import puurrtybot.databases.database_queries as ddq
from puurrtybot import ROLES_FAMILY
import puurrtybot


HIDDEN_STATUS = True


class FamilyManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ctx_id = {}

    @cog_ext.cog_slash(
        name = "join_family",
        description = "join_family",
        options = [
            create_option(
                            name = "family_name",
                            description = "family_name",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = key, value = str(value)) for key, value in sorted(ROLES_FAMILY.items())])
                   ]
                      )
    async def join_pack(self, ctx:SlashContext, family_name: str):
        family_name = int(family_name)
        n = ddq.get_trait_role_qualify(family_name , ctx.author_id)
        s = {1:''}.get(n, 's')
        if n>0:
            new_role = puurrtybot.GUILD.get_role(family_name)
            try:
                old_role = [role for role in ctx.author.roles if role.id in ROLES_FAMILY.values()][0]
                await ctx.author.remove_roles(old_role)
            except IndexError:
                pass
            await ctx.author.add_roles(new_role)
            content = f"""{ctx.author.mention}, you have {n} qualifying cat{s}. You joined {new_role}."""
        else:
            content = f"""{ctx.author.mention} can't join, because you have {n} cat{s} with the trait needed."""
        await ctx.send(content, hidden=HIDDEN_STATUS)
        

def setup(client):
    client.add_cog(FamilyManager(client))