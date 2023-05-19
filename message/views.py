import os

import discord

import manager
from config import bot


class ArticleUpload(discord.ui.View):

    def __init__(self, filename, content, author):
        super().__init__()
        self.filename = filename
        self.content = content
        self.author = author

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button, interaction):
        embed = discord.Embed()
        guild_id = interaction.guild_id
        if not os.path.exists(f"articles/{guild_id}/"):
            os.makedirs(f"articles/{guild_id}/")
        if os.path.isfile(f"articles/{guild_id}/{self.filename}"):
            embed.color = 0x8e0000
            embed.description = "Un article sur ce sujet existe déjà."
        else:
            with open(f"articles/{guild_id}/{self.filename}", "w") as file:
                file.write(self.content)
            manager.register_article(self.filename, self.author, guild_id)
            embed.color = 0x008e00
            embed.description = "Votre article a été correctement enregistré."
        self.clear_items()
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)

