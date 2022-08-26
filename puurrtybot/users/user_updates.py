import puurrtybot
import puurrtybot.api.blockfrost as blockfrost
import puurrtybot.database.query as dq
import puurrtybot.database.insert as di

#from puurrtybot import ROLES_BASED_ON_TRAITS, ROLES_BASED_ON_FAMILY, ROLES_NUMBER_OF_CATS, ROLES_NUMBER_OF_CATS_DICT

 
async def user_update_role_number_of_cats(user_id):
    n_cats = dq.get_user_number_of_assets(user_id)
    match = 0
    for n_role, role_id in sorted(list(ROLES_NUMBER_OF_CATS_DICT.items())):
        if n_cats < n_role:
            break;
        else:
            match = role_id

    member = puurrtybot.GUILD.get_member(int(user_id))
    try:
        old_role = [role for role in member.roles if role.id in ROLES_NUMBER_OF_CATS][0]
        await member.remove_roles(old_role)
    except IndexError:
        pass
    new_role = puurrtybot.GUILD.get_role(match)
    await member.add_roles(new_role)


async def user_update_roles_all(user_id):
    member = puurrtybot.GUILD.get_member(int(user_id))
    member_role_ids = [role.id for role in member.roles]

    # ROLES_NUMBER_OF_CATS
    await user_update_role_number_of_cats(user_id)


    # ROLES_BASED_ON_TRAITS
    for role_id in ROLES_BASED_ON_TRAITS:
        n = dq.get_trait_role_qualify(role_id, user_id)
        if n > 0:
            if role_id not in member_role_ids:
                await member.add_roles(puurrtybot.GUILD.get_role(role_id))
        else:
            if role_id in member_role_ids:
                await member.remove_roles(puurrtybot.GUILD.get_role(role_id))


    # ROLES_BASED_ON_FAMILY
    family_roles = [role_id for role_id in member_role_ids if role_id in ROLES_BASED_ON_FAMILY]
    for role_id in family_roles:
        if 0 == dq.get_trait_role_qualify(role_id, user_id):
            await member.remove_roles(puurrtybot.GUILD.get_role(role_id))   


def user_update_addresses(user_id):
    user = dq.get_user_by_user_id(user_id)
    stake_addresses = set([address.stake_address for address in user.addresses])
    addresses = [address.address for address in user.addresses]
    for stake_address in stake_addresses:
        new_addresses = [address for address in blockfrost.get_address_list_by_stake_address(stake_address) if address not in addresses]
        for new_address in new_addresses:
            di.new_address_stake_address(new_address, stake_address, user_id)