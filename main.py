import src.core.correction as correction
import src.core.file_system as file_system

from pathlib import Path


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
    workspace = r"C:\Users\mathi\Desktop\Prépa\Entrainement pour la rentrée\Entrainement MP2I"
    TD_dir = Path(workspace) / "TD"
    TD_corriges_dir = Path(workspace) / "TD corrigés"
    TD_name = "Sommes & Calculs Algébriques"
    ex_number = 1
    
    correction = correction.Correction(file_system.Path_Settings(workspace, TD_dir, TD_corriges_dir, TD_name))
    correction.correct(ex_number)
