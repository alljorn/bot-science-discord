import os

import discord
from discord import InputTextStyle
from discord.ui import InputText

from database import ArticleDatabase


class WriteModal(discord.ui.Modal):

    def __init__(self, title):
        super().__init__(title=title)
        self.add_item(InputText(label="Titre"))
        self.add_item(InputText(label="Text", style=InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        database = ArticleDatabase()
        embed = discord.Embed()
        if os.path.isfile(f"articles/{self.children[0].value}"):
            embed.color = 0xc90000
            embed.description = "Un article sur ce sujet existe déjà."
        else:
            with open(f"articles/{self.children[0].value}", "w") as file:
                file.write(self.children[1].value)
            database.register_article(self.children[0].value,
                                      interaction.user.id)
            embed.color = 0x00c900
            embed.description = "Votre article a été correctement enregistré."
        await interaction.response.send_message(embed=embed)
