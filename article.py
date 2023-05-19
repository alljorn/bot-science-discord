import os
from datetime import datetime

import discord
from discord.ext import commands

import manager
from algorithm import levenshtein_distance
from message.embeds import *
from message.modals import WriteModal


class Article(commands.Cog):

    article = discord.SlashCommandGroup("article")

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @article.command(description="Supprimer un article")
    async def delete(self, ctx, title):
        if not os.path.isfile(f"articles/{ctx.guild_id}/{title}"):
            embed = discord.Embed(
                color=0x8e0000,
                description="Il n'existe pas encore d'article sur ce sujet."
                )
            await ctx.respond(embed=embed)
            return
        director_id = manager.get_director_role(ctx.guild_id)
        if not director_id in [role.id for role in ctx.user.roles]:
            embed = discord.Embed(
                color=0x8e0000, title="Permission Manquant",
                description="Veuillez contacter un admin pour vous enregistrez " \
                "en tant que director sur le bot.")
        else:
            os.remove(f"articles/{ctx.guild_id}/{title}")
            embed = discord.Embed(color=0x005865,
                                  description="L'article a bien été retiré.")
        await ctx.respond(embed=embed)

    @article.command(description="Trouver un article")
    async def search(self, ctx, author: discord.User):
        cursor = manager.DATA_BASE.cursor()
        cursor.execute(f"SELECT * FROM article WHERE guild = {ctx.guild_id} " \
                       f"AND author = {author.id}")
        articles = cursor.fetchall()
        embed = discord.Embed(color=0x005865)
        if articles:
            embed.title = f"Article de {author.name}"
            text = ""
            for article in articles:
                text += f"« {article[0]} » le {datetime.fromtimestamp(article[2])}\n"
            embed.description = text
        else:
            embed.description = f"{author.name} n'a pas encore écrit d'articles."
        await ctx.respond(embed=embed)

    @article.command(description="Parcourez les articles du Science bot !")
    async def recent(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(color=0x0a5865)
        global articles
        articles = manager.get_recent_articles(ctx.guild_id)
        if articles:
            embed.title = "Choisissez un article :"
            class ArticleSelect(discord.ui.View):
                global info_dict
                info_dict = {info[0]: info for info in articles}

                def __init__(self, timeout, bot):
                    super().__init__(timeout=timeout)
                    self.bot = bot

                async def on_timeout(self):
                    self.clear_items()
                    try:
                        await self.message.edit(view=self)
                    except discord.HTTPException:
                        pass

                @discord.ui.select(options=[discord.SelectOption(label=info)
                                              for info in info_dict])
                async def select_callback(self, select, interaction):
                    info = info_dict[select.values[0]]
                    with open(f"articles/{info[3]}/{info[0]}") as file:
                        text = file.read()
                    embed = discord.Embed(color=0x0a5865, title=info[0],
                                          description=text)
                    user = await self.bot.fetch_user(info[1])
                    embed.timestamp = datetime.fromtimestamp(info[2])
                    embed.set_footer(text=user.name, icon_url=user.avatar.url)
                    await interaction.response.send_message(embed=embed)

            await ctx.respond(embed=embed, view=ArticleSelect(15, self.bot))
        else:
            embed.title = "Soyez le premier à en écrire un !"
            await ctx.respond(embed=embed)

    @article.command(description="Lire un article")
    async def read(self, ctx: discord.ApplicationContext, title):
        embed = discord.Embed(color=0x005865)
        cursor = manager.DATA_BASE.cursor()
        cursor.execute(f"SELECT * FROM article WHERE guild = {ctx.guild_id}")
        articles = cursor.fetchall()
        if not articles:
            embed.title = "Soyez le premier à en écrire un !"
            await ctx.respond(embed=embed)
        matched = [(levenshtein_distance(title.lower(), article[0].lower()), article) for article in articles]
        matched.sort()
        if matched[0][0] == 0:
            article = matched[0][1]
            embed.title = article[0]
            with open(f"articles/{ctx.guild_id}/{article[0]}") as file:
                embed.description = file.read()
            user = await self.bot.fetch_user(article[1])
            embed.timestamp = datetime.fromtimestamp(article[2])
            embed.set_footer(text=user.name, icon_url=user.avatar.url)
            await ctx.respond(embed=embed)
            return
        elif matched:
            embed.title = "Choisissez un article :"
            class ArticleSelect(discord.ui.View):
                global info_dict
                info_dict = {info[1][0]: info[1] for info in matched[:10]}

                def __init__(self, timeout, bot):
                    super().__init__(timeout=timeout)
                    self.bot = bot

                async def on_timeout(self):
                    self.clear_items()
                    try:
                        await self.message.edit(view=self)
                    except discord.HTTPException:
                        pass

                @discord.ui.select(options=[discord.SelectOption(label=info)
                                              for info in info_dict])
                async def select_callback(self, select, interaction):
                    info = info_dict[select.values[0]]
                    with open(f"articles/{info[3]}/{info[0]}") as file:
                        text = file.read()
                    embed = discord.Embed(color=0x0a5865, title=info[0],
                                          description=text)
                    user = await self.bot.fetch_user(info[1])
                    embed.timestamp = datetime.fromtimestamp(info[2])
                    embed.set_footer(text=user.name, icon_url=user.avatar.url)
                    await interaction.response.send_message(embed=embed)

            await ctx.respond(embed=embed, view=ArticleSelect(15, self.bot))
        else:
            embed.description = "Ancun article n'existe avec ce titre."
            await ctx.respond(embed=embed)

    @article.command(description="Écrivez un article sur la science")
    async def write(self, ctx: discord.ApplicationContext):
        writer_id = manager.get_writer_role(ctx.guild_id)
        if not writer_id in [role.id for role in ctx.user.roles]:
            embed = discord.Embed(
                color=0x8e0000, title="Permission Manquant",
                description="Veuillez contacter un admin pour vous enregistrez " \
                "en tant que writer sur le bot.")
            await ctx.respond(embed=embed)
        else:
            modal = WriteModal("Rédaction d'un article")
            await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(Article(bot))
