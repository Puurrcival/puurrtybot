import asyncio
from typing import List

import discord
from discord.ext import commands, tasks
import tqdm

import puurrtybot
from puurrtybot.api import blockfrostio, twitter
from puurrtybot.database import query as dq, update as du, insert as di
from puurrtybot.database.create import Address, User
from puurrtybot.helper import functions as hf
from puurrtybot.pcs.role import ID_2_ROLE, Family, Status


def update_asset_all():
    outdated_assets = dq.get_asset_all(hf.get_utc_time()-24*60*60)
    for asset in tqdm.tqdm(outdated_assets):
        asset.address = blockfrostio.get_address_by_asset(asset.asset_id)
        du.update_object(asset)


def update_address_all_by_user(user: User):
    addresses: List[Address] = dq.fetch_row_by_value(Address, Address.user_id, user.user_id, all=True)
    addresses_address = [address.address for address in addresses]
    if addresses:
        stake_addresses = set([address.stake_address for address in addresses if address.stake_address])
        for stake_address in stake_addresses:
            for address in blockfrostio.get_address_list_by_stake_address(stake_address):
                if address not in addresses_address:
                    di.insert_row(Address(address, stake_address, user.user_id))


def update_twitter_by_user(user: User):
    if user.twitter_id:
        user.twitter_handle = twitter.get_username_by_twitter_id(user.twitter_id)
        du.update_object(user)


async def update_role_all_by_user(user: User):
        member = puurrtybot.GUILD.get_member(user.user_id)
        member_role_dict = {role.id:role for role in member.roles}
        roles = dq.get_role_by_user_id(user.user_id)
        remove_roles = []
        add_roles = [puurrtybot.DISCORD_ROLES[Status.VERIFIED.value.role_id]]
        for role in roles:
            if not role.requirement and member_role_dict.get(role.role_id):
                # Member is not eligible, but has role
                remove_roles.append(member_role_dict.get(role.role_id))
            elif role.requirement and not member_role_dict.get(role.role_id) and type(ID_2_ROLE.get(role.role_id)) is not Family:
                # Member is eligible, but hasn't role and roles isn't Family
                if puurrtybot.DISCORD_ROLES.get(role.role_id, None): add_roles.append(puurrtybot.DISCORD_ROLES[role.role_id])
                pass
        if remove_roles:
            await member.remove_roles(*remove_roles)
        if add_roles:
            await member.add_roles(*add_roles)


async def update_user(user: User):
    update_address_all_by_user(user)
    update_twitter_by_user(user)
    await update_role_all_by_user(user)


class UpdateManager(commands.Cog):
    """Updating the database and discord roles."""
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot

    async def static_loop(self):
        print('UpdateManager running')
        if dq.get_asset_all(hf.get_utc_time()-4*60*60):
            await asyncio.to_thread(update_asset_all)
            print("""Update Roles""")
            for user in tqdm.tqdm(dq.fetch_table(User)):
                """Update Roles.""" 
                await update_user(user)


    @commands.Cog.listener()
    async def on_ready(self):
        new_task = tasks.loop(seconds = 10*60, count = None)(self.static_loop)
        new_task.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UpdateManager(bot), guilds = [discord.Object(id = 998148160243384321)])