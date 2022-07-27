import puurrtybot, json



#new functions


##################
def user_get_assets_n(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
    try:    
        return user['assets_n']
    except KeyError:
        return 0


def user_get_stakes(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
    try:    
        return '\n'.join(user['stakes'])
    except KeyError:
        return 0 


def user_get_twitter(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
    try:
        return list(user['twitter'].keys())[0]
    except KeyError:
        return False


def user_get_twitter_id(userid):
    user_dir= f"""{puurrtybot.PATH}/puurrtybot/databases/users/"""
    with open(f"""{user_dir}{userid}.json""", 'r') as openfile:
        user = json.load(openfile)
    try:
        return list(user['twitter'].values())[0]
    except KeyError:
        return False


def get_address_by_asset(asset):
    asset_dir = f"""{puurrtybot.PATH}/puurrtybot/databases/assets_by_name/"""
    with open(f"""{asset_dir}{asset.split('.')[0]}.json""", 'r') as openfile:
        return json.load(openfile)['address']