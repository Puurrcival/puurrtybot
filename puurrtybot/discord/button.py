import discord
from discord.ext import commands


class button_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.member)
    
    @discord.ui.button(label = "verify", style = discord.ButtonStyle.green, custom_id = "verify_button")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user
        bucket = self.cooldown.get_bucket(interaction.message)
        retry = bucket.update_rate_limit()
        if retry:
            return await interaction.response.send_message(f"""Cooldown! Try again in {round(retry,1)} seconds.""", ephemeral=True)
        else:
            return await interaction.response.send_message(f"""check""", ephemeral=True)