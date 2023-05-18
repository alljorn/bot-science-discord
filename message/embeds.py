import os

import discord

import manager


class WelcomeConfigEmbed(discord.Embed):

    def __init__(self):
        super().__init__(
            title="Bienvenu sur Science bot !",
            description=
"""Merci d'avoir ajouté le bot au serveur !
Pour profiter pleinement de toutes les fonctionnalités, une configuration est nécessaire.""",
            color=0x0a5865
        )
        self.add_field(
            name="__Étape 1:__",
            value=
"""> Configurer un rôle *directeur de rédaction* 
**effectuez la commande `set_director`**
*ce rôle permettra à un utilisateur de gérer tous articles du serveur*""",
            inline=False
        )
        self.add_field(
            name="__Étape 2:__",
            value=
"""> Configurer un rôle *rédacteur*
**effectuez la commande `set_writer`**
*ce rôle permettra à un utilisateur d'écrire des articles*"""
        )
        self.set_footer(text="Profitez bien du bot !")


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
        super().__init__(color=0x0a5865,
                         title="Paramètres de configuration du serveur",
                         description="")

        director_role_id = manager.get_director_role(guild.id)
        if director_role_id:
            self.description += f"Rôle directeur de rédaction: <@&{director_role_id}>\n\n"
        else:
            self.description += "Rôle directeur de rédaction: **aucun rôle défini**\n" \
                                "*effectuez la commande* `/set_director`\n\n"

        writer_role_id = manager.get_writer_role(guild.id)
        if writer_role_id:
            self.description += f"Rôle rédacteur: <@&{writer_role_id}>"
        else:
            self.description += "Rôle réacteur: **aucun rôle défini**\n" \
                                "*effectuez la commande* `/set_writer`"
