import puurrtybot, json
import puurrtybot.blockfrost.blockfrost_queries as bbq
import puurrtybot.databases.database_functions as ddf


JOIN_TRAITS = {"Kitsune": True, 
                "Zombie": True, 
                "Wizard Hat": True, 
                "Wand": True, 
                "Halo": True, 
                "Angel Wings": True, 
                "Crystal": True, 
                "Cyborg": True, 
                "Devil": True, 
                "Fire Eyes": True, 
                "Devil Tail": True, 
                "Gold": True, 
                "Jason": True, 
                "Crown": True, 
                "Pharaoh Headress": True,
                "Skeleton": True,
                "Yes": True,
                "Pirate Hat": True,
                "Pirate Jacket": True,
                "Laser Eyes":True}

def user_update_addresses(user_id, save=False):
    address_list = []
    for stake_address in puurrtybot.USERS[user_id]['stakes']:
        address_list += bbq.get_address_list_by_stake_address(stake_address)


    for address in puurrtybot.USERS[user_id]['addresses']:
        if address not in address_list:
            stake_address += bbq.get_stake_address_by_address(address)
            puurrtybot.USERS[user_id]['stakes'] += stake_address
            address_list += bbq.get_address_list_by_stake_address(stake_address)

    puurrtybot.USERS[user_id]['addresses'] = list(set(puurrtybot.USERS[user_id]['addresses'] + address_list))
    puurrtybot.USERS[user_id]['stakes'] = list(set(puurrtybot.USERS[user_id]['stakes']))


def user_update_assets(user_id):
    assets = []
    for address in puurrtybot.USERS[user_id]['addresses']:
        try:
            assets += puurrtybot.ASSETS_ADDRESSES[address]
        except KeyError:
            pass
    assets = list(set(assets))
    puurrtybot.USERS[user_id]['assets'] = assets
    puurrtybot.USERS[user_id]['assets_n'] = len(assets)


def user_update_traits(user_id):
    traits = {}
    join_trait = {}
    for asset in puurrtybot.USERS[user_id]['assets']:
        join_trait_done = {}
        for k,v in puurrtybot.ASSETS[asset]['onchain_metadata'].items():
            k = k.strip()
            v = v.strip()
            if k not in ['name', 'image', 'mediaType', 'collection'] and v!='':
                try:
                    traits[k]
                except KeyError:
                    traits[k] = {}

                # join_trait
                if v in JOIN_TRAITS.keys():
                    v = puurrtybot.JOIN_TRAITS[v]
                    try:
                        join_trait_done[v]
                    except KeyError:
                        join_trait_done[v] = True
                        try:
                            join_trait[v] += 1
                        except KeyError:
                            join_trait[v] = 1


                try:
                    traits[k][v]+=1
                except KeyError:
                    traits[k][v] =1
    try:
        traits['unique'] = traits['unique']['Yes']
    except KeyError:
        pass
    puurrtybot.USERS[user_id]['traits'] = traits
    puurrtybot.USERS[user_id]['join_trait'] = join_trait


def save_user(user_id):
    dic = {user_id: puurrtybot.USERS[user_id]}
    with open(f"""{puurrtybot.USERS_DIR}/{user_id}.json""", 'w') as json_file:
        json.dump(dic, json_file)


def new_user(user_id):
    user_id = str(user_id)
    puurrtybot.USERS.update( {user_id : {"addresses":[], "stakes": [], "twitter": {}} })
    save_user(user_id)


def user_update(user_id):
    user_update_addresses(user_id)
    user_update_assets(user_id)
    user_update_traits(user_id)
    save_user(user_id)


def user_all_update():
    for user_id in puurrtybot.USERS.keys():
        user_id = str(user_id)
        user_update(user_id)
    ddf.save_users()