import discord

import manager
from config import token, bot
from message.embeds import *

bot.load_extension("article")


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt.")


@bot.slash_command(description="Définissez le rôle directeur de rédaction de ce serveur")
async def set_director(ctx: discord.ApplicationContext, role: discord.Role):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=AdministratorPermissionErrorEmbed())
        return
    manager.set_director_role(ctx.guild_id, role.id)
    await ctx.respond(embed=SetDirectorSuccesEmbed(role))


@bot.slash_command(description="Définissez le rôle redacteur de ce serveur")
async def set_writer(ctx: discord.ApplicationContext, role: discord.Role):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=AdministratorPermissionErrorEmbed())
        return
    manager.set_writer_role(ctx.guild_id, role.id)
    await ctx.respond(embed=SetWritterSuccesEmbed(role))


@bot.slash_command(description="Affiche les paramamètres de configuration du bot")
async def show_config(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    await ctx.respond(embed=ShowConfigEmbed(ctx.guild))


bot.run(token)
