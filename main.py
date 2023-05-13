# -*- coding: utf-8 -*-

import discord

from setting import token


bot = discord.Bot()

def read_article(path):
    with open(path, "r", encoding='utf8') as fichier:
	    return fichier.read()


@bot.event
async def on_ready():
    print(f"{bot.user.name} est prêt")

@bot.slash_command(name = "article", description = "Affiche les articles récent")
async def print_article(ctx: discord.ApplicationContext):
    class article_embed(discord.Embed):
        def __init__(self):
                super().__init__(
                    title = "aucun article sélectionné",
                    description="vide"
                )
    class article_view(discord.ui.View):
            async def on_timeout(self) -> None:
                self.disable_all_items()
                await ctx.interaction.edit_original_response(view=self)
            
            @discord.ui.select(
                placeholder = "voir les articles ", # titre
                # nombre de choix minimum et maximum
                min_values = 1,
                max_values=1,
                # ajout des options
                options = [
                    discord.SelectOption(
                        label="Quitter",
                        description="Retourner à la salle de pause"
                    )]
                    + [
                    discord.SelectOption( # choix d'achat des produits de l'inventaire du ditributeur
                        label=path, # le nom
                        description=title
                    ) for title, path in article_data
                    ]
            )
            async def select_callback(self, select: discord.ui.Select, interaction: discord.Interaction):
                if select.values[0] == "Quitter":
                    await interaction.response.edit_message(view=None)
                else:
                    embed =  discord.Embed(
                        title = select.values[0],
                        description=read_article(select.values[0]))
                    await interaction.response.edit_message(view=article_view(), embed=embed)
    await ctx.respond(embed=article_embed(), view=article_view())


# (Titre de l'article, chemin relatif vers le fichier)
article_data = [
    ("Que sont les trous noirs ?", "que sont les trous noirs.txt"),
    ("Comment les trous noirs absorbent la matière", "comment les trous noirs absorbent la matière.txt"),
    ("De quoi sont composés les nuages", "de quoi sont composés les nuages.txt"),
    ("Comment la vie est-elle née", "comment la vie est-elle née.txt"),
    ("Pourquoi les dinosaures ont-ils disparu", "pourquoi les dinosaures ont-ils disparu.txt"),
    ("Pourquoi le ciel est-il bleu", "pourquoi le ciel est-il bleu.txt"),
    ("Comment fonctionne le soleil", "comment fonctionne le soleil.txt")
]


bot.run(token)