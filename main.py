import discord

import manager
from config import token, bot
from message.embeds import *
from message.views import InitializeButton


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt.")


@bot.event
async def on_guild_join(guild: discord.Guild):
    if not manager.is_guild_exists(guild.id):
        manager.add_guild(guild.id)
        for text_channel in guild.text_channels:
            if text_channel.can_send():
                embed = WelcomeConfigEmbed()
                await text_channel.send(embed=embed)
                return

    
@bot.slash_command(description="Définissez le rôle directeur de rédaction de ce serveur")
async def set_director(ctx: discord.ApplicationContext, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=AdministratorPermissionErrorEmbed())
    else:
        manager.set_director_role(ctx.guild_id, role.id)
        await ctx.respond(embed=SetDirectorSuccesEmbed(role))


@bot.slash_command(description="Définissez le rôle redacteur de ce serveur")
async def set_writer(ctx: discord.ApplicationContext, role: discord.Role):
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=AdministratorPermissionErrorEmbed())
    else:
        manager.set_writer_role(ctx.guild_id, role.id)
        await ctx.respond(embed=SetWritterSuccesEmbed(role))


@bot.slash_command(description="Affiche les paramamètres de configuration du bot")
async def show_config(ctx: discord.ApplicationContext):
    await ctx.respond(embed=ShowConfigEmbed(ctx.guild))


if __name__ == "__main__":
    for guild in bot.guilds:
        if not manager.is_guild_exists(guild.id):
            manager.add_guild(guild.id)
    bot.load_extension("article")
    bot.run(token)
