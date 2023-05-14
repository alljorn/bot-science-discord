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
    user = await bot.fetch_user(772448700097232907)
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

    embed = articleEmbed()
    await ctx.respond(embed=embed)




bot.run(token)