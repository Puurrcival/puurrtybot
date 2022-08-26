from calendar import c
from discord.ext import commands, tasks
import tqdm
import puurrtybot

import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.database.query as dq
import puurrtybot.database.update as du
import puurrtybot.database.insert as di
from puurrtybot.database.create import User
import puurrtybot.helper.functions as func
from puurrtybot.pcs.role import ID_2_ROLE, Family
from puurrtybot import DISCORD_ROLES


async def update_asset_all():
    outdated_assets = dq.get_asset_all(func.get_utc_time()-24*60*60)
    for asset in tqdm.tqdm(outdated_assets):
        address = blockfrost.get_address_by_asset(asset.asset_id)
        du.update_address_by_asset_id(asset.asset_id, address)


async def update_address_all_by_user(user: User):
    addresses = dq.get_address_by_user_id(user.user_id)
    stake_addresses = set([address.stake_address for address in addresses if address.stake_address])
    addresses = set([address.address for address in addresses])
    for stake_address in stake_addresses:
        for address in blockfrost.get_address_list_by_stake_address(stake_address):
            if address not in addresses:
                di.new_address_stake_address(address, stake_address, user.user_id)


async def update_role_all_by_user(user: User):
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
                add_roles.append(DISCORD_ROLES[role.role_id])
        if remove_roles:
            await member.remove_roles(*remove_roles)
        if add_roles:
            await member.add_roles(*add_roles)


async def update_user(user: User):
    await update_address_all_by_user(user)
    user = dq.get_user_by_user_id(user.user_id)
    await update_role_all_by_user(user)


class UpdateManager(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def static_loop(self):
        print('UpdateManager running')
        if dq.get_asset_all(func.get_utc_time()-24*60*60):
            """Update Assets."""
            await update_asset_all()

            """Update Addresses."""
            users = dq.get_user_all()   
            for user in tqdm.tqdm(users):
                await update_address_all_by_user(user)

            """Update Roles."""
            users = dq.get_user_all()   
            for user in tqdm.tqdm(users):
                await update_role_all_by_user(user)

    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 10*60, count = None)(self.static_loop)
        new_task.start()


def setup(client):
    client.add_cog(UpdateManager(client))