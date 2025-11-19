
import json
from analyser import main
import sys



import json 
# Assurez-vous d'importer la fonction 'main'
# from .votre_module import main 

def execute_analysis():
    print("=== Analyseur SmartDebug ===\n")

    #  Demander les valeurs à l'utilisateur
    PROJECT_PATH = input("Chemin du projet : ").strip()
    SCRIPT_NAME = input("Nom du script à analyser : ").strip()
    ENV_NAME = input("Nom de l'environnement virtuel (env par défaut) : ").strip()

    if ENV_NAME == "":
        ENV_NAME = "env"

    print(f"\nDémarrage de l'analyse pour le script: {SCRIPT_NAME}")
    print(f"Projet : {PROJECT_PATH}")
    print(f"Environnement : {ENV_NAME}\n")

    print(f"Démarrage de l'analyse pour le script: {SCRIPT_NAME} dans {PROJECT_PATH} avec l'environnement {ENV_NAME}")

    try:
        # Appel de la fonction main. On suppose que 'main' retourne le dictionnaire.
        result_json = main(
            project_path=PROJECT_PATH,
            script_name=SCRIPT_NAME,
            env_name=ENV_NAME
        )
        
        # Affichage du résultat JSON
        print("\n--- Résultat JSON de l'analyse ---")
        # Utiliser json.dumps pour une belle mise en forme
        print(json.dumps(result_json, indent=4, ensure_ascii=False))

        # ✅ CORRECTION : Retourne le résultat pour qu'il soit utilisé par l'appelant
        return result_json
        
    except Exception as e:
        print(f"\n Une erreur inattendue est survenue lors de l'exécution : {e}")
        # En cas d'erreur, il est préférable de retourner None ou un dictionnaire vide 
        # pour éviter de crasher l'appelant si celui-ci ne vérifie pas 'None'.
        return None

if __name__ == "__main__":
    execute_analysis()