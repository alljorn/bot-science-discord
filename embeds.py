import os
from datetime import datetime

import discord

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
"""| Configurer un rôle *director*
**effectuer la commande `set_director`**
*le rôle défini sera celui permettant un utilisateur de faire entre autre le management des articles du serveur*""",
        )
        self.add_field(
            name=
"__Étape 3:__",
            value=
"""| Configurer un rôle *writter*
**effectuer la commande `set_writter`**
*le rôle défini sera celui autorisant un utilisateur à écrire des artcicles*"""
        )
        self.set_footer(
            text=
"Profitez bien de Science bot !"
        )


class InitializeErrorEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title="Oups...",
            description="Science bot n'a pas été initialisé, demandez à un administreur"
        )


class ArticleEmbed(discord.Embed):

    def __init__(self):
        super().__init__(title="Parcourez les articles du Science Bot !")
        database = ArticleDatabase()
        articles = database.get_recent_articles()
        articles = [f"«{info[0]}» par <@{info[1]}> " \
                    f"le {datetime.fromtimestamp(info[2])}"
                    for info in articles]
        if articles:
            self.description = "- ".join(articles)
        else:
            self.description = "Soyez le premier à écrire !"
