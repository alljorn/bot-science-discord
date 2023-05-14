import os

import discord

import manager
from database import ArticleDatabase
from embeds import WelcomeConfigEmbed


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
            color=0x00e500
        )  
        self.disable_on_timeout = False
        response = interaction.response
        await response.edit_message(embeds=[WelcomeConfigEmbed(), embed])


class ArticleUpload(discord.ui.View):

    def __init__(self, filename, content, author):
        super().__init__()
        self.filename = filename
        self.content = content
        self.author = author

    @discord.ui.button(label="Confirmer", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button, interaction):
        database = ArticleDatabase()
        embed = discord.Embed()
        guild_id = interaction.guild_id
        if not os.path.exists(f"articles/{guild_id}"):
            os.makedirs(f"articles/{guild_id}")
        if os.path.isfile(f"articles/{guild_id}/{self.filename}"):
            embed.color = 0xe50000
            embed.description = "Un article sur ce sujet existe déjà."
        else:
            with open(f"articles/{guild_id}/{self.filename}", "w") as file:
                file.write(self.content)
            database.register_article(self.filename, self.author, guild_id)
            embed.color = 0x00e500
            embed.description = "Votre article a été correctement enregistré."
        await interaction.response.send_message(embed=embed)
        self.clear_items()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Annuler", style=discord.ButtonStyle.red)
    async def cancel_callback(self, button, interaction):
        self.clear_items()
        await interaction.response.edit_message(view=self)
