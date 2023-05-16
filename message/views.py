import os

import discord

import manager
from config import bot
from message.embeds import WelcomeConfigEmbed


class InitializeButton(discord.ui.View):

    def __init__(self, author_id, guild_id):
        super().__init__(disable_on_timeout=True, timeout=30)
        self.author_id = author_id
        self.guild_id = guild_id
    
    @discord.ui.button(label="Initialiser Science bot sur ce serveur",
                       style=discord.ButtonStyle.blurple)
    async def confirm_callback(self, button: discord.ui.Button,
                               interaction: discord.Interaction):
        if interaction.user.id != self.author_id: return
        manager.add_guild(self.guild_id)
        embed = discord.Embed(
            title = "Félicitation !",
            description = "Science bot est maintenant initialisé sur le serveur !",
            color=0x008e00
        )  
        self.disable_on_timeout = False
        self.clear_items()
        await interaction.response.edit_message(
            embeds=[WelcomeConfigEmbed(), embed], view=self
            )


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
        if not os.path.exists(f"articles/{guild_id}/{self.author}"):
            os.makedirs(f"articles/{guild_id}/{self.author}")
        if os.path.isfile(f"articles/{guild_id}/{self.author}/{self.filename}"):
            embed.color = 0x8e0000
            embed.description = "Un article sur ce sujet existe déjà."
        else:
            with open(f"articles/{guild_id}/{self.author}/{self.filename}", "w") as file:
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

