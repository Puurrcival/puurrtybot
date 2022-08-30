from discord.ext import commands, tasks
import discord

from puurrtybot.helper import image_handle
from puurrtybot.database import insert as di, query as dq
from puurrtybot.database.create import User
from puurrtybot.discord.cogs.updatemanager import update_role_all_by_user
from discord.ui import Button, View


PUURRDO_ANSWER = {}



class MemberVerifier(commands.Cog):
    def __init__(self, bot: commands.bot.Bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    #    if payload.channel_id == 998148162277625918 and payload.message_id == 1013945235446968362 and str(payload.emoji) == "🔎":
    #        user_id = payload.user_id)
    #        member = self.client.get_member(user_id


    # @cog_ext.cog_slash(
    #     name = "verify",
    #     description = "verify")
    # async def meet_puurrdo(self, ctx: SlashContext):
    #     1013945235446968362
    #     if dq.fetch_row(User(ctx.author_id)):
    #         await ctx.send("""You are already verified.""")
    #     else:
    #         image, answer = image_handle.puurrdo()
    #         PUURRDO_ANSWER[ctx.author_id] = str(answer)
    #         embed = discord.Embed(title=f"""**Where is Puurrdo?**""", description="Find Puurrdo in the image and solve with: **/verify_solve**", color=0x109319)
    #         image_files = [discord.File(image, filename="puurrdo.png"),
    #                         discord.File(image_handle.get_asset_image("f96584c4fcd13cd1702c9be683400072dd1aac853431c99037a3ab1e5075757272646f"), filename="thumbnail.png")]
            
    #         embed.set_thumbnail(url=f"""attachment://thumbnail.png""")
    #         embed.set_image(url=f"""attachment://puurrdo.png""")
    #         await ctx.send(embed = embed, files = image_files, hidden=True)

    # @cog_ext.cog_slash(
    # name = "verify_solve",
    # description = "verify_solve",
    # options = [create_option(
    #                     name = "solve",
    #                     description = "solve",
    #                     required = True,
    #                     option_type = 3,
    #                     choices = [create_choice(name = str(solution), value = str(solution)) for solution in range(1,25)])
    #             ])
    # async def find_puurrdo(self, ctx: SlashContext, solve: str):
    #     user_id = ctx.author_id
    #     if PUURRDO_ANSWER.get(user_id, None) == solve:
    #         new_user = User(user_id = user_id, username = ctx.author)
    #         di.insert_row(new_user)
    #         await update_role_all_by_user(new_user)
    #         await ctx.send('Right!', hidden = True)
    #     else:
    #         await ctx.send('False!', hidden = True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemberVerifier(bot), guilds = [discord.Object(id = 998148160243384321)])