
import json
from analyser import main
import sys

# Ajouter le répertoire parent si nécessaire pour l'importation, si le fichier groq_analyser.py n'est pas dans le même répertoire
# sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

# Importer la fonction main depuis votre fichier de code (que nous appellerons 'groq_analyser.py')
# Assurez-vous d'avoir enregistré le code précédent dans ce fichier !


def execute_analysis():
    # --- Vos paramètres spécifiques ---
    PROJECT_PATH = "C:/Users/lemda/Documents/test"
    SCRIPT_NAME = "test.py"
    ENV_NAME = "env"

    print(f"Démarrage de l'analyse pour le script: {SCRIPT_NAME} dans {PROJECT_PATH} avec l'environnement {ENV_NAME}")

    try:
        # Appel de la fonction main
        result_json = main(
            project_path=PROJECT_PATH,
            script_name=SCRIPT_NAME,
            env_name=ENV_NAME
        )
        
        # Affichage du résultat JSON
        print("\n--- Résultat JSON de l'analyse ---")
        # Utiliser json.dumps pour une belle mise en forme
        print(json.dumps(result_json, indent=4, ensure_ascii=False))
        
    except Exception as e:
        print(f"\n Une erreur inattendue est survenue lors de l'exécution : {e}")

if __name__ == "__main__":
    execute_analysis()