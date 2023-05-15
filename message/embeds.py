import os

import discord
import manager


class WelcomeConfigEmbed(discord.Embed):
    def __init__(self):
        super().__init__(
            title=
"Bienvenu sur Science bot !",
            description=
"""Merci d'avoir ajouté le bot au serveur !
Pour profiter pleinement de toutes les fonctionnalités, une configuration est nécessaire.""",
            color=0x0a5865
        )
        self.add_field(
            name=
"__Étape 1:__",
            value=
"""> Initialiser le bot
**utiliser le bouton `Initialiser Science bot sur ce serveur`**
*ainsi le serveur sera enregistré dans la base de données de Science bot*""",
            inline=False
        )
        self.add_field(
            name=
"__Étape 2:__",
            value=
"""> Configurer un rôle *directeur de rédaction* 
**effectuez la commande `set_director`**
*ce rôle permettra à un utilisateur de gérer tous articles du serveur*""",
            inline=False
        )
        self.add_field(
            name=
"__Étape 3:__",
            value=
"""> Configurer un rôle *rédacteur*
**effectuez la commande `set_writer`**
*ce rôle permettra à un utilisateur d'écrire des articles*"""
        )
        self.set_footer(
            text=
"Profitez bien du bot !"
        )


class InitializeSuccesEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title = "Félicitation !",
            description = "Science bot est maintenant initialisé sur le serveur !",
            color=0x008e00
        )

class InitializeErrorEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title="Oups...",
            description="Science bot n'a pas été initialisé, demandez à un administreur"
        )


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
            color=0x008e00
        )


class SetWritterSuccesEmbed(discord.Embed):

    def __init__(self, role: discord.Role):
        super().__init__(
            title="Félicitation !",
            description = f"Les {role.mention} sont maintenant rédacteurs sur le serveur !",
            color=0x008e00
        )


class ShowConfigEmbed(discord.Embed):

    def __init__(self, guild: discord.Guild):
        super().__init__(
            title="Paramètres de configuration du serveur",
            color=0x0a5865
        )
        director_role_id = manager.get_director_role(guild.id)
        self.add_field(
            name="__rôle *directeur de rédaction*:__",
            value=f"`{director_role_id}`: @{guild.get_role(director_role_id)}" if director_role_id is not None \
            else "*aucun rôle défini*\n**effectuez la commande `set_director`**",
            inline=False
        )
        writer_role_id = manager.get_writer_role(guild.id)
        self.add_field(
            name="__rôle *rédacteur*:__",
            value=f"`{writer_role_id}`: @{guild.get_role(writer_role_id)}" if writer_role_id is not None \
            else "*aucun rôle défini*\n**effectuez la commande `set_writer`**"
        )
