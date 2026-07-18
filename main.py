from src.ui import ui

"""
TODO: 
 - visualisation des performances du pc (RAM, CPU, GPU, etc...)

WORKFLOW:

1. L'utilisateur sélectionne un fichier Markdown à corriger.
2. Le fichier est lu et son contenu est passé au modèle de langage.
3. Le modèle génère la correction en français, avec les formules en LaTeX.
4. La correction est ajoutée après chaque exercice.
5. Le document corrigé est sauvegardé.

"""


if __name__ == "__main__":
    ui.launch_app()
