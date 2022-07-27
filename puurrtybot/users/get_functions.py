import puurrtybot


def user_get_n_cats(user_id):
    return puurrtybot.USERS[str(user_id)]['assets_n']


def user_get_traits(user_id):
    return puurrtybot.USERS[str(user_id)]['traits']


def user_get_stakes(user_id):
    return ', '.join(puurrtybot.USERS[str(user_id)]['stakes'])
