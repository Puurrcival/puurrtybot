import discord

import puurrtybot
from puurrtybot.pcs.role import Status
from puurrtybot.database import insert as di
from puurrtybot.database.create import User

class PuurrdoSelect(discord.ui.View):
    @discord.ui.select(
        placeholder = "Coose the tile with Puurrdo.",
        options = [discord.SelectOption(label = str(number), value = str(number)) for number in range(1,25)]
        )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        if int(select.values[0]) == puurrtybot.PUURRDO_ANSWER[interaction.user.id]:
            await interaction.user.add_roles(puurrtybot.DISCORD_ROLES[Status.VERIFIED.value.role_id])
            di.insert_row(User(interaction.user.id))
            await interaction.response.send_message(content=f"""You found Puurrdo.""")
        else:
            await interaction.response.send_message("""That is not Puurrdo, you may try again.""", ephemeral=True)