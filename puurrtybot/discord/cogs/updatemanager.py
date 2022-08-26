from discord.ext import commands, tasks
import tqdm
import puurrtybot

import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.database.query as dq
import puurrtybot.database.update as du
import puurrtybot.helper.functions as func
from puurrtybot.pcs.role import ID_2_ROLE, Family


class UpdateManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('UpdateManager running')
        print("""Update Assets.""")
        outdated_assets = dq.get_asset_all(func.get_utc_time()-24*60*60)
        for asset in tqdm.tqdm(outdated_assets):
            address = blockfrost.get_address_by_asset(asset.asset_id)
            du.update_address_by_asset_id(asset.asset_id, address)

        print("""Update Roles.""")
        users = dq.get_user_all()
        discord_roles = {role.id: role for role in puurrtybot.GUILD.roles}
        for user in tqdm.tqdm(users):
            member = puurrtybot.GUILD.get_member(user.user_id)
            member_role_dict = {role.id:role for role in member.roles}
            roles = dq.get_role_by_user_id(user.user_id)
            remove_roles = []
            add_roles = []
            for role in roles:
                if not role.requirement and member_role_dict.get(role.role_id):
                    # Member is not eligible, but has role
                    remove_roles.append(member_role_dict.get(role.role_id))
                elif role.requirement and not member_role_dict.get(role.role_id) and type(ID_2_ROLE.get(role.role_id)) is not Family:
                    # Member is eligible, but hasn't role and roles isn't Family
                    add_roles.append(discord_roles[role.role_id])
            if remove_roles:
                await member.remove_roles(*remove_roles)
            if add_roles:
                await member.add_roles(*add_roles)

    @commands.Cog.listener()
    async def on_ready(self):
        self.channel = self.client.get_channel(1003641743117406278)
        new_task = tasks.loop(seconds = 10*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(UpdateManager(client))