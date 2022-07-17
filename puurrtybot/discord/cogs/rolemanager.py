from discord.ext import commands, tasks
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
import random, datetime
#import puurrtybot.blockchain.verify_queries as pbq
#import puurrtybot.database.verify_queries as pdq

HIDDEN_STATUS = True

class RoleManager(commands.Cog):

    def __init__(self, client):
        self.client = client

    
def setup(client):
    client.add_cog(RoleManager(client))