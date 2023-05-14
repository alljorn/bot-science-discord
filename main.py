# -*- coding: utf-8 -*-

import discord

import manager
from config import token, bot
from embeds import *
from modals import WriteModal
from views import *



@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt")


async def initialize_guild(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        embed = WelcomeConfigEmbed()
        view  = initialize_button(ctx.author.id, ctx.guild_id)
    else:
        embed = InitializeErrorEmbed()
        view  = None
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(description="parcourez les articles du Science bot !")
async def article(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
    else:
        embed = ArticleEmbed()
        await ctx.respond(embed=embed)


@bot.slash_command(description="Écrivez un article sur la science")
async def write(ctx: discord.ApplicationContext):
    # manque la vérification de rôle
    modal = WriteModal("Rédaction d'un article")
    await ctx.send_modal(modal)


bot.run(token)
