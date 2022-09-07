import discord

class WalletModal(discord.ui.Modal, title="Placeholder"):
    answer = discord.ui.TextInput(label = "Enter your Cardano address or ada handle", style=discord.TextStyle.short, placeholder="addr1.../$handle", default="nothing", required=True, max_length=150)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await interaction.followup.send(f"""{self.answer}""".strip(), ephemeral=True)