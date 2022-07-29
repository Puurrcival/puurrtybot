import puurrtybot


def user_get_n_cats(user_id):
    return puurrtybot.USERS[f"""{user_id}"""]['assets_n']


def user_get_traits(user_id):
    return puurrtybot.USERS[f"""{user_id}"""]['traits']


def user_get_stakes(user_id):
    return ', '.join(puurrtybot.USERS[f"""{user_id}"""]['stakes'])


def user_get_trait_n(user_id, trait):
    try:
        return puurrtybot.USERS[f"""{user_id}"""]['join_trait'][trait]
    except KeyError:
        return 0


def user_get_twitter(user_id, get_value = "id"):
    try:
        return puurrtybot.USERS[f"""{user_id}"""]['twitter'][get_value]
    except KeyError:
        return None