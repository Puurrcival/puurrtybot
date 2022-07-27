import puurrtybot
import puurrtybot.users.get_functions as ugf


def match_roles_n(n_cats):
    n_cats = int(n_cats)
    match = 0
    for n_role, role_id in sorted(list(puurrtybot.ROLES_N_DICT.items())):
        if n_cats < n_role:
            break;
        else:
            match = role_id
    return match


def get_n_role(user_id):
    user_id = str(user_id)
    n_cats = ugf.user_get_n_cats(user_id)
    return match_roles_n(n_cats)
