# -*- coding: utf-8 -*-

import discord
import manager
from config import token, bot
from embeds import *
from views import *



@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt")


async def initialize_guild(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        embed = welcomeConfigEmbed()
        view  = initialize_button(ctx.author.id, ctx.guild_id)
    else:
        embed = initializeErrorEmbed()
        view  = None
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="article", description="parcourez les articles du Science bot !")
async def article(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return

    await ctx.respond(embed=articleEmbed())

@bot.slash_command(name="set_director", description="définissez le rôle directeur de rédaction de ce serveur")
async def set_director(ctx: discord.ApplicationContext, role: discord.Role):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=administratorPermissionErrorEmbed())
        return
    manager.set_director_role(ctx.guild_id, role.id)
    await ctx.respond(embed=setDirectorSuccesEmbed(role))

@bot.slash_command(name="set_writter", description="définissez le rôle redacteur de ce serveur")
async def set_writter(ctx: discord.ApplicationContext, role: discord.Role):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond(embed=administratorPermissionErrorEmbed())
        return
    manager.set_writter_role(ctx.guild_id, role.id)
    await ctx.respond(embed=setWritterSuccesEmbed(role))


@bot.slash_command(name="show_config", description="Affiche les paramamètres de configuration du bot")
async def show_config(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    await ctx.respond(embed=showConfigEmbed(ctx.guild))



bot.run(token)