import os
from datetime import datetime

import discord
import manager

from database import ArticleDatabase


class WelcomeConfigEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title=
"Bienvenu sur le Science bot !",
            description=
"""Merci d'avoir ajouté Science bot au serveur !
Pour profiter pleinement de toutes les fonctionnalités une configuration est nécessaire""",
            color=discord.Color.from_rgb(0, 0, 255)
        )
        self.add_field(
            name=
"__Étape 1:__",
            value=
"""| Initialiser le bot
**utiliser le bouton `Initialiser Science bot sur ce serveur`**
*ainsi le serveur sera enregistré dans la base de données de Science bot*""",
            inline=False
        )
        self.add_field(
            name=
"__Étape 2:__",
            value=
"""| Configurer un rôle *directeur de rédaction* 
**effectuez la commande `set_director`**
*le rôle défini sera celui permettant un utilisateur de faire entre autre le management des articles du serveur*""",
        )
        self.add_field(
            name=
"__Étape 3:__",
            value=
"""| Configurer un rôle *rédacteur*
**effectuez la commande `set_writter`**
*le rôle défini sera celui autorisant un utilisateur à écrire des artcicles*"""
        )
        self.set_footer(
            text=
"Profitez bien de Science bot !"
        )


class InitializeSuccesEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title = "Félicitation !",
            description = "Science bot est maintenant initialisé sur le serveur !",
            color=discord.Color.from_rgb(0, 255, 0)
        )

class InitializeErrorEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title="Oups...",
            description="Science bot n'a pas été initialisé, demandez à un administreur"
        )


class ArticleEmbed(discord.Embed):

    def __init__(self):
        super().__init__(color=0x0a5060,
                         title="Parcourez les articles du Science Bot !")
        database = ArticleDatabase()
        articles = database.get_recent_articles()
        articles = [f"« {info[0]} » par <@{info[1]}> " \
                    f"le {datetime.fromtimestamp(info[2])}"
                    for info in articles]
        if articles:
            self.description = "- ".join(articles)
        else:
            self.description = "Soyez le premier à écrire !"


class AdministratorPermissionErrorEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title="Oups...",
            description="Vous n'êtes pas autorisé à effectuer cette commande, demandez à un administreur"
        )


class SetDirectorSuccesEmbed(discord.Embed):

    def __init__(self, role: discord.Role):
        super().__init__(
            title="Félicitation !",
            description = f"Les {role.mention} sont maintenant directeurs de rédaction sur le serveur !",
            color=discord.Color.from_rgb(0, 255, 0)
        )


class SetWritterSuccesEmbed(discord.Embed):

    def __init__(self, role: discord.Role):
        super().__init__(
            title="Félicitation !",
            description = f"Les {role.mention} sont maintenant rédacteurs sur le serveur !",
            color=discord.Color.from_rgb(0, 255, 0)
        )


class ShowConfigEmbed(discord.Embed):

    def __init__(self, guild: discord.Guild):
        super().__init__(
            title="Paramètres de configuration du serveur",
            color=discord.Color.from_rgb(255, 255, 225)
        )
        director_role_id = manager.get_director_role(guild.id)
        self.add_field(
            name="__rôle *directeur de rédaction*:__",
            value=f"`{director_role_id}`: @{guild.get_role(director_role_id)}" if director_role_id is not None else "*aucun rôle défini*\n**effectuez la commande `set_director`**",
            inline=False
        )
        writter_role_id = manager.get_writter_role(guild.id)
        self.add_field(
            name="__rôle *rédacteur*:__",
            value=f"`{writter_role_id}`: @{guild.get_role(writter_role_id)}" if writter_role_id is not None else "*aucun rôle défini*\n**effectuez la commande `set_writter`**"
        )
