import puurrtybot
import puurrtybot.roles.get_functions as rgf

async def update_roles_n(guild, user_id):
    for user_id in puurrtybot.USERS.keys():
        member = guild.get_member(int(user_id))
        new_role_id = int(rgf.get_n_role(user_id))
        new_role = guild.get_role(new_role_id)
        await member.add_roles(new_role)

        # remove old roles
        for role in member.roles:
            if role.id in puurrtybot.ROLES_N.keys() and role.id != new_role.id:
                await member.remove_roles(role)