"""A module that contains user-related classes"""
import puurrtybot.databases.database_queries as ddq
import puurrtybot.functions as func
import puurrtybot

class User:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        #self.member = puurrtybot.GUILD.get_member(user_id)
        data = ddq.get_user_by_id(user_id)
        self.assets = func.flatten_list([address.assets for address in data.addresses if address.assets])