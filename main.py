# -*- coding: utf-8 -*-

import discord

import manager
from config import token, bot
from message.embeds import *
from message.modals import WriteModal
from message.views import *


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt")


async def initialize_guild(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        embed = WelcomeConfigEmbed()
        view  = InitializeButton(ctx.author.id, ctx.guild_id)
    else:
        embed = InitializeErrorEmbed()
        view  = None
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(description="Parcourez les articles du Science bot !")
async def article(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
    else:
        await ctx.respond(embed=ArticleEmbed(), view=ArticleSelect())

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
    manager.set_writter_role(ctx.guild_id, role.id)
    await ctx.respond(embed=SetWritterSuccesEmbed(role))


@bot.slash_command(description="Affiche les paramamètres de configuration du bot")
async def show_config(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
        return
    await ctx.respond(embed=ShowConfigEmbed(ctx.guild))

@bot.slash_command(description="Écrivez un article sur la science")
async def write(ctx: discord.ApplicationContext):
    # manque la vérification de rôle
    modal = WriteModal("Rédaction d'un article")
    await ctx.send_modal(modal)


bot.run(token)
