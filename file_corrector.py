import os
import json
import operator
# Assurez-vous que 'from debugging import execute_analysis' est correct
from debugging import execute_analysis 


class FileCorrector:
    def __init__(self, file_to_fix: str):
        self.file_to_fix = file_to_fix

    # -------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------
    def load_lines(self):
        """Charge toutes les lignes du fichier à corriger."""
        with open(self.file_to_fix, "r", encoding="utf-8") as f:
            return f.readlines()

    def save_lines(self, lines):
        """Sauvegarde les lignes corrigées et crée un backup."""
        backup = self.file_to_fix + ".backup"
        # On utilise try/except car os.rename peut échouer si le fichier n'existe pas
        try:
             os.rename(self.file_to_fix, backup)
        except FileNotFoundError:
             # Si le fichier n'existe pas encore, on crée juste le backup vide
             with open(backup, "w", encoding="utf-8") as f:
                 pass
             
        with open(self.file_to_fix, "w", encoding="utf-8") as f:
            f.writelines(lines)

        print(f"✔ Modifications appliquées. Backup créé : {backup}")

    # -------------------------------------------------------------
    # Patch Logic
    # -------------------------------------------------------------
    def apply_patch(self):
        print("\n📡 Appel de l’analyse IA...")
        patch_data = execute_analysis()  # Le résultat est un dictionnaire attendu

        # Vérification contre le retour None
        if patch_data is None:
            print("❌ L'analyse IA a échoué. Le résultat de l'analyse est None.")
            return

        # Vérification du format JSON attendu
        if "errors" not in patch_data:
            print("❌ JSON invalide : pas de clé 'errors'")
            return

        lines = self.load_lines()
        new_lines = lines.copy()

        # Tri des corrections par numéro de ligne décroissant (du bas vers le haut).
        # C'est CRUCIAL : les modifications sur les lignes inférieures ne changent pas l'index des lignes supérieures.
        errors_to_apply = sorted(
            patch_data["errors"], 
            key=lambda x: int(x.get("line_error", 0)), 
            reverse=True 
        )
        
        for err in errors_to_apply:
            fixed_line = err.get("fixed_line", "").rstrip("\n")

            # -------------------------------------------------
            # 1. Extraction et validation du numéro de ligne (entier)
            # -------------------------------------------------
            try:
                line_number = int(err.get("line_error"))
            except (TypeError, ValueError):
                print(f"⚠ Erreur ignorée (line_error invalide ou N/A): {err.get('line_error')}")
                continue

            # Conversion du numéro de ligne (base 1) en index de liste (base 0)
            line_index = line_number - 1 
            
            print(f"\n➡ Correction de : {err.get('explanation', '(pas d’explication)')} à la ligne {line_number}")

            # Vérification de l'index dans la liste
            if line_index < 0 or line_index >= len(new_lines):
                print(f"⚠ Numéro de ligne {line_number} hors limites. Ajout de la ligne corrigée en fin de fichier.")
                new_lines.append(fixed_line + "\n")
                continue

            # -------------------------------------------------
            # 2. Remplacement de la ligne erronée avec gestion de l'indentation
            # -------------------------------------------------
            
            original_line = new_lines[line_index]
            
            # **Extraction de l'indentation** (espaces au début de la ligne)
            indentation = original_line[:len(original_line) - len(original_line.lstrip())]
            
            # Affichage de la ligne originale avant correction
            print(f"   Ligne originale (L{line_number}, Indentation: {len(indentation)} espaces): '{original_line.strip()}'")
            
            # Application de l'indentation à la ligne corrigée
            corrected_line_with_indentation = indentation + fixed_line + "\n"
            
            # Remplacement direct de l'élément à l'index
            new_lines[line_index] = corrected_line_with_indentation

            print(f"✔ Ligne corrigée insérée : '{corrected_line_with_indentation.strip()}'")


        self.save_lines(new_lines)


# -------------------------------------------------------------
# Execution directe
# -------------------------------------------------------------
if __name__ == "__main__":
    # L'utilisateur choisit le fichier à corriger
    filepath = input("Chemin du fichier à corriger : ").strip()

    fixer = FileCorrector(file_to_fix=filepath)
    fixer.apply_patch()