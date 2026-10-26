import json
import os

FILENAME = "scores.json"


def charger_scores():
    """Lecture des scores directement structurés en JSON."""
    if not os.path.exists(FILENAME):
        return []
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def ajouter_score(nom, score):
    """Ajoute le score dans la structure de dictionnaires JSON."""
    scores = lire_scores()
    # On stocke sous forme de dictionnaire clé/valeur (3 lettres max)
    scores.append({"name": nom.upper()[:3], "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)
