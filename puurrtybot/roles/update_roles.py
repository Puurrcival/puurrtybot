import puurrtybot
import puurrtybot.roles.get_functions as rgf
from puurrtybot.variables import ROLES_TRAITS

async def update_roles_n(guild):
    for user_id in puurrtybot.USERS.keys():
        member = guild.get_member(int(user_id))
        new_role_id = int(rgf.get_n_role(user_id))
        new_role = guild.get_role(new_role_id)
        await member.add_roles(new_role)

        # remove old roles
        for role in member.roles:
            if role.id in puurrtybot.ROLES_N.keys() and role.id != new_role.id:
                await member.remove_roles(role)

async def update_roles_traits(guild):
    for user_id in puurrtybot.USERS.keys():
        member = guild.get_member(int(user_id))
        member_role_ids = [role.id for role in member.roles]
        for role_id in puurrtybot.ROLES_TRAITS.keys():
            try:
                puurrtybot.USERS[user_id]['traits'][ROLES_TRAITS[role_id][0]][ROLES_TRAITS[role_id][1]]
                if role_id not in member_role_ids:
                    await member.add_roles(guild.get_role(role_id))
            except KeyError:
                if role_id in member_role_ids:
                    await member.remove_roles(guild.get_role(role_id))
