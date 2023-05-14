import discord
import manager
from embeds import *


class initialize_button(discord.ui.View):
    def __init__(self, author_id, guild_id):
        super().__init__(disable_on_timeout=True, timeout=30)
        self.author_id = author_id
        self.guild_id = guild_id
    
    @discord.ui.button(label="Initialiser Science bot sur ce serveur", style=discord.ButtonStyle.blurple)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id != self.author_id: return
        manager.add_guild(self.guild_id)
        self.disable_on_timeout = False
        await interaction.response.edit_message(embeds=[welcomeConfigEmbed(), initializeSuccesEmbed()], view=None)