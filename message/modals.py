import discord

from message.views import ArticleUpload


class WriteModal(discord.ui.Modal):

    def __init__(self, title):
        super().__init__(title=title)
        self.add_item(discord.ui.InputText(label="Titre"))
        self.add_item(discord.ui.InputText(
            label="Text", style=discord.InputTextStyle.long,
            placeholder="N'oubliez pas de sauvegarder un brouillon.")
                      )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(color=0x0a5865,
                              title=self.children[0].value,
                              description=self.children[1].value)
        embed.set_footer(text=interaction.user.name,
                         icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(
            embed=embed,
            view=ArticleUpload(self.children[0].value, self.children[1].value,
                               interaction.user.id)
            )
