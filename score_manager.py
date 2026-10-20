import json
import os

FICHIER_SCORES = "scores.json"

def charger_scores():
    """Charge les scores depuis le fichier JSON. Retourne une liste."""
    # Si le fichier n'existe pas encore, on retourne une liste vide
    if not os.path.exists(FICHIER_SCORES):
        return []
    
    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        # En cas de fichier corrompu ou illisible, on repart à zéro
        return []

def sauvegarder_nouveau_score(nom, score_joueur):
    """Ajoute un score, trie le tableau et garde le Top 5 ou Top 10."""
    # 1. Charger les anciens scores
    liste_scores = charger_scores()
    
    # 2. Ajouter le nouveau score sous forme de dictionnaire
    nouveau_donnee = {"name": nom.upper()[:3], "score": score_joueur} # Force 3 lettres max
    liste_scores.append(nouveau_donnee)
    
    # 3. Trier la liste du plus grand score au plus petit
    # La fonction lambda indique à Python de trier en se basant sur la clé "score"
    liste_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # 4. Optionnel : Limiter le Hall of Fame au Top 5 pour rester lisible
    liste_scores = liste_scores[:5]
    
    # 5. Réécrire le fichier JSON proprement
    with open(FICHIER_SCORES, "w", encoding="utf-8") as f:
        # indent=4 permet d'avoir le format joli avec les retours à la ligne
        json.dump(liste_scores, f, indent=4, ensure_ascii=False)
