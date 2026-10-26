import json
import os
import tkinter as tk
from tkinter import messagebox

FILENAME = "scores.json"


def lire_scores():
    """Lecture des scores directement structurés en JSON."""
    if not os.path.exists(FILENAME):
        return []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            # json.load convertit directement le fichier en une liste Python
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def ajouter_score(nom, score):
    """Ajoute le score dans la structure de dictionnaires JSON."""
    scores = lire_scores()

    # On stocke sous forme de dictionnaire clé/valeur
    scores.append({"name": nom.upper()[:3], "score": score})

    # Tri basé sur la clé "score" de chaque dictionnaire, limité au Top 10
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    # Écriture propre du fichier structuré
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4, ensure_ascii=False)


def valider_score():
    nom = entry_nom.get().strip()
    try:
        score = int(entry_score.get())
    except ValueError:
        messagebox.showerror("Erreur", "Le score doit être un nombre.")
        return

    if not nom:
        messagebox.showerror("Erreur", "Le nom ne peut pas être vide.")
        return

    ajouter_score(nom, score)
    messagebox.showinfo("Succès", f"Score ajouté pour {nom} !")
    afficher_scores()


def afficher_scores():
    scores = lire_scores()
    texte = "🏆 Meilleurs scores :\n\n"
    # On lit directement les clés du dictionnaire sans faire de .split()
    for i, donnees in enumerate(scores, start=1):
        texte += f"{i}. {donnees['name']} — {donnees['score']}\n"
    label_scores.config(text=texte)


# --- Interface graphique (Tkinter) ---
root = tk.Tk()
root.title("Meilleurs Scores (Version JSON)")
root.geometry("400x400")
root.resizable(False, False)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Nom :").grid(row=0, column=0, padx=5, pady=5)
entry_nom = tk.Entry(frame)
entry_nom.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Score :").grid(row=1, column=0, padx=5, pady=5)
entry_score = tk.Entry(frame)
entry_score.grid(row=1, column=1, padx=5, pady=5)

btn_valider = tk.Button(root, text="Ajouter Score", command=valider_score)
btn_valider.pack(pady=10)

label_scores = tk.Label(root, text="", font=("Courier", 12), justify="left")
label_scores.pack(padx=10, pady=10)

afficher_scores()
root.mainloop()
