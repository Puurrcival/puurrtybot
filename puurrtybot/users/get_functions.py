import puurrtybot


def user_get_n_cats(user_id):
    return puurrtybot.USERS[str(user_id)]['assets_n']


def user_get_traits(user_id):
    return puurrtybot.USERS[str(user_id)]['traits']


def user_get_stakes(user_id):
    return ', '.join(puurrtybot.USERS[str(user_id)]['stakes'])


def user_get_trait_n(user_id, trait):
    user_id = str(user_id)
    try:
        return puurrtybot.USERS[user_id]['join_trait'][trait]
    except KeyError:
        return 0