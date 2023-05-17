import os
from datetime import datetime

import discord
from discord.ext import commands

import manager
from message.embeds import *
from message.modals import WriteModal
from message.views import InitializeButton


class Article(commands.Cog):

    article = discord.SlashCommandGroup("article")

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def guild_missing(self, ctx):
        if not manager.is_guild_exists(ctx.guild_id):
            if ctx.author.guild_permissions.administrator:
                embed = WelcomeConfigEmbed()
                view  = InitializeButton(ctx.author.id, ctx.guild_id)
            else:
                embed = InitializeErrorEmbed()
                view  = None
            await ctx.respond(embed=embed, view=view)
            return True
        return False

    @article.command(description="Trouver un article")
    async def search(self, ctx, author: discord.User):
        if await self.guild_missing(ctx):
            return
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
        if await self.guild_missing(ctx):
            return
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
        if await self.guild_missing(ctx):
            return
        if not os.path.isfile(f"articles/{ctx.guild_id}/{title}"):
            embed = discord.Embed(
                color=0x8e0000,
                description="Il n'existe pas encore d'article sur ce sujet."
                )
        else:
            cursor = manager.DATA_BASE.cursor()
            cursor.execute(f"SELECT author, timestamp FROM article " \
                           f"WHERE title = \"{title}\" AND guild = {ctx.guild_id}")
            article = cursor.fetchone()
            embed = discord.Embed(
                color=0x005865,
                title=title
                )
            with open(f"articles/{ctx.guild_id}/{title}") as file:
                embed.description = file.read()
            user = await self.bot.fetch_user(article[0])
            embed.timestamp = datetime.fromtimestamp(article[1])
            embed.set_footer(text=user.name, icon_url=user.avatar.url)
        await ctx.respond(embed=embed)

    @article.command(description="Écrivez un article sur la science")
    async def write(self, ctx: discord.ApplicationContext):
        if await self.guild_missing(ctx):
            return
        writer_id = manager.get_writer_role(ctx.guild_id)
        if not writer_id in [role.id for role in ctx.user.roles]:
            embed = discord.Embed(
                color=0x8e0000, title="Permission Manquant",
                description="Veuillez contacter un admin pour vous enregistrez " \
                "en tant que director ou writer sur le bot.")
            await ctx.respond(embed=embed)
        else:
            modal = WriteModal("Rédaction d'un article")
            await ctx.send_modal(modal)


def setup(bot):
    bot.add_cog(Article(bot))
