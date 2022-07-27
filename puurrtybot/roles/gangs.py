import puurrtybot


def get_kitsune(user_id):
    user_id = str(user_id)
    try:
        return puurrtybot.USERS[user_id]['traits']['mask']['Kitsune']
    except KeyError:
        return 0


async def join_kitsune(guild, user_id, trait = "Kitsune"):
    user_id = str(user_id)
    trait_n = get_kitsune(user_id)
    member = guild.get_member(int(user_id))
    member_roles = [role for role in member.roles]
    new_role_id = int(puurrtybot.ROLES_TRAITS[trait])
    new_role = guild.get_role(new_role_id)
    print(new_role)

    if new_role in member_roles:
        return f"Already in {trait}"

    if trait_n > 0:
        await member.add_roles(new_role)
        return f"Joined {trait}"

    return f"You don't have {trait} Trait"




