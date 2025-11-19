from get_stack import run_in_venv

import json
import os
import requests
from typing import Tuple
api_key = os.getenv("GROQ_API_KEY")

prompt_path = "prompt.txt"
# ------------------------------------------------------------
# Charger le prompt depuis un fichier
# ------------------------------------------------------------
def load_prompt(prompt_path: str) -> str:
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------
# Appeler Groq LLM avec ton prompt + données
# ------------------------------------------------------------
def call_agent(api_key: str, system_prompt: str, user_content: str) -> dict:
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen/qwen3-32b",   # Tu peux changer de modèle
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API error: {response.text}")

    content = response.json()["choices"][0]["message"]["content"]

    # Vérifier que c’est bien un JSON
    try:
        # L'IA pourrait ajouter des ```json...``` autour du JSON. On tente de nettoyer.
        if content.strip().startswith("```json") and content.strip().endswith("```"):
            content = content.strip()[7:-3].strip()
            
        return json.loads(content)
    except json.JSONDecodeError:
        # En cas d'erreur de décodage JSON, on capture la réponse brute de l'IA pour le debug
        raise ValueError(f" L'IA n'a pas retourné un JSON valide. Réponse brute : \n{content}")


# ------------------------------------------------------------
# Fonction principale : analyse erreur + code, renvoie JSON
# ------------------------------------------------------------
def analyze_and_get_json(
    api_key: str,
    prompt_path: str,
    project_path: str,
    script_name: str,
    env_name: str = "env"
) -> dict:
    
    
    # Charger le prompt system
    system_prompt = load_prompt(prompt_path)

    # Exécuter ton script dans le venv
    print(f"🔬 Exécution de {script_name} pour capturer les erreurs...")
    stdout, stderr = run_in_venv(project_path, script_name, env_name)

    # Si pas d’erreur → inutile de demander à l’IA
    if not stderr.strip():
        # Utiliser l'erreur pour la construction du prompt même s'il n'y en a pas
        stderr = "Aucune erreur n’a été trouvée dans la sortie."
    else:
        print("🚨 Erreurs détectées, préparation du message pour l'IA.")
    
    # Lire le code original
    script_path = os.path.join(project_path, script_name)
    with open(script_path, "r", encoding="utf-8") as f:
        original_code = f.read()

    # Construire le message utilisateur
    user_message = f"""
Code original :
---
{original_code}
---

Erreurs (stderr) :
---
{stderr}
---
"""

    # Appeler l'agent Groq
    print(" Appel de l'agent Groq pour l'analyse...")
    try:
        response_json = call_agent(api_key, system_prompt, user_message)
        print("✅ Réponse JSON reçue de l'agent Groq.")
        return response_json
    except Exception as e:
        print(f"❌ Erreur lors de l'appel à Groq ou lors du traitement de la réponse : {e}")
        # Renvoyer une structure d'erreur qui respecte le format demandé pour l'échec
        return {
            "status": "invalid",
            "line_error": "N/A",
            "explanation": f"Échec de l'appel à l'API Groq ou réponse non-JSON : {str(e)}",
            "fixed_line": "N/A",
            "summary": "Échec de l'analyse."
        }


# ------------------------------------------------------------
# Fonction principale pour exécuter l'analyse
# ------------------------------------------------------------
def main(project_path: str, script_name: str, env_name: str = "env") -> dict:
    """
    Exécute le script, analyse les erreurs avec Groq et retourne le JSON d'analyse.
    """
    print(f" Démarrage de l'analyse pour le script : {script_name} dans {project_path}")
    
    # 1. Analyser le code et l'erreur avec l'IA et obtenir le JSON
    analysis_json = analyze_and_get_json(api_key, prompt_path, project_path, script_name, env_name)
    
    return analysis_json