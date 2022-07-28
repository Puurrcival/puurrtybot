import puurrtybot


def get_kitsune(user_id):
    user_id = str(user_id)
    try:
        return puurrtybot.USERS[user_id]['traits']['mask']['Kitsune']
    except KeyError:
        return 0


async def join_trait(new_role, ctx, user_id, trait, trait_n):
    trait = trait.title()
    user_id = str(user_id)
    member = ctx.author
    try:
        member_roles = [role for role in ctx.author.roles if role.id in puurrtybot.ROLES_TRAITS.values()][0]
        print(member_roles)
    except IndexError:
        member_roles = None
    print(new_role, member_roles)

    if new_role == member_roles:
        return f"Already in {trait}"

    elif trait_n > 0:
        await member.add_roles(new_role)
        if member_roles:
            await member.remove_roles(member_roles)
        return f"Joined {new_role} and left {member_roles}"

    else:
        return f"You don't have {trait} Trait"




