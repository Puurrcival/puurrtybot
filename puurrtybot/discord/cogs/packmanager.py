from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice
import puurrtybot.users.get_functions as ugf
import puurrtybot.roles.packs as prg
import puurrtybot


HIDDEN_STATUS = True


class PackManager(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ctx_id = {}

    @cog_ext.cog_slash(
        name = "join_pack",
        description = "join_pack",
        options = [
            create_option(
                            name = "pack_name",
                            description = "pack_name",
                            required = True,
                            option_type = 3,
                            choices = [create_choice(name = pack, value = pack.lower()) for pack in sorted(puurrtybot.ROLES_JOIN_TRAITS.keys())])
                   ]
                      )
    async def join_pack(self, ctx:SlashContext, pack_name: str):
        n = ugf.user_get_trait_n(ctx.author_id, pack_name)
        s = {1:''}.get(n, 's')
        user_id = ctx.author_id
        self.ctx_id[user_id] = ctx
        if n>0:
            new_role = puurrtybot.GUILD.get_role(int(puurrtybot.ROLES_JOIN_TRAITS[pack_name.title()]))
            content = await prg.join_trait(new_role, ctx.author, pack_name, n)
            content = f"""{ctx.author.mention}, you have {n} qualifying cat{s}. {content}"""
        else:
            content = f"""{ctx.author.mention} can't join {pack_name}, because you have {n} cat{s} with the trait needed."""
        await self.ctx_id[user_id].send(content, hidden=HIDDEN_STATUS)
        

def setup(client):
    client.add_cog(PackManager(client))