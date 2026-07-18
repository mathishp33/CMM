from src.ui import ui

"""
TODO: 
 - interface CMD stylé avec : 
   - fenetre pour sélectionner le fichier à corriger
   - visualisation des performances du pc (RAM, CPU, GPU, etc...)
   - des messages à l'utilisateur pour l'informer du stade de la correction (init, lecture, correction, écriture, finit)
 

WORKFLOW:

1. L'utilisateur sélectionne un fichier Markdown à corriger.
2. Le fichier est lu et son contenu est passé au modèle de langage.
3. Le modèle génère la correction en français, avec les formules en LaTeX.
4. La correction est ajoutée après chaque exercice.
5. Le document corrigé est sauvegardé.

"""


if __name__ == "__main__":
    ui.launch_app()
