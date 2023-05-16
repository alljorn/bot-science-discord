from datetime import datetime

import discord

import manager
from config import token, bot
from message.embeds import *
from message.modals import WriteModal
from message.views import InitializeButton


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt.")


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
        embed = discord.Embed(color=0x0a5865)
        articles = manager.get_recent_articles()
        if articles:
            embed.title = "Choisissez un article :"
            class ArticleSelect(discord.ui.View):
                global info_dict
                info_dict = {info[0]: info for info in manager.get_recent_articles()}

                async def on_timeout(self):
                    self.clear_items()
                    try:
                        await self.message.edit(view=self)
                    except discord.HTTPException:
                        pass

                @discord.ui.select(options = [discord.SelectOption(label=info) for info in info_dict])
                async def select_callback(self, select, interaction):
                    info = info_dict[select.values[0]]
                    with open(f"articles/{info[3]}/{info[1]}/{info[0]}") as file:
                        text = file.read()
                    embed = discord.Embed(color=0x0a5865, title=info[0], description=text)
                    user = await bot.fetch_user(info[1])
                    embed.timestamp = datetime.fromtimestamp(info[2])
                    embed.set_footer(text=user.name, icon_url=user.avatar.url)
                    await interaction.response.send_message(embed=embed)

            await ctx.respond(embed=embed, view=ArticleSelect(timeout=15))
        else:
            embed.title = "Soyez le premier à en écrire un !"
            await ctx.respond(embed=embed)


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


@bot.slash_command(description="Écrivez un article sur la science")
async def write(ctx: discord.ApplicationContext):
    if not manager.is_guild_exists(ctx.guild_id):
        await initialize_guild(ctx)
    else:
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


bot.run(token)
