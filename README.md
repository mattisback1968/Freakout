# 🕹️ Breakout Retro Edition

Une adaptation moderne et fidèle du grand classique du retrogaming **Breakout**, développée en **Python** avec la bibliothèque **Pygame**. Le jeu se lance directement dans une fenêtre dédiée sur votre bureau.

## 🚀 Fonctionnalités
- **Gameplay Classique** : Détruisez toutes les briques en faisant rebondir la balle sur votre raquette.
- **Affichage Bureau** : Fenêtré avec des graphismes et une palette de couleurs inspirés des bornes d'arcade rétro.
- **Gestion des Vies & Score** : Suivi en direct du score et du nombre de billes restantes.
- **Évolution de la Difficulté** : La vitesse de la balle augmente au fil des briques détruites.

## 🛠️ Pré-requis

Pour lancer ce jeu, vous devez avoir installé :
- **Python 3.12** (version 3.8 ou supérieure recommandée)
- **Pygame**

## 📦 Installation

1. **Cloner le projet** sur votre machine :
   ```bash
   git clone https://github.com
   cd NOM_DE_VOTRE_DEPOT
   ```

2. **Installer les dépendances** nécessaires (Pygame) :
   ```bash
   pip install pygame
   ```

## 🎮 Utilisation

Pour lancer le jeu depuis votre terminal, exécutez la commande suivante :
```bash
python main.py
```

### ⌨️ Commandes du jeu
- **Flèche Gauche (`←`)** : Déplacer la raquette vers la gauche
- **Flèche Droite (`→`)** : Déplacer la raquette vers la droite
- **Espace** : Lancer la balle au début de la partie / Relancer après une vie perdue / Mettre en pause / Sortir du mode Pause
- **Échap (`Éch`)** : Quitter le jeu à tout moment

## 🎼 Les Niveaux & Clins d'œil Culturels

Chaque niveau de cette adaptation possède sa propre identité visuelle et est nommé d'après un clin d'œil musical, cinématographique, littéraire ou populaire. 

Voici quelques exemples de niveaux que vous devrez affronter :
* **"Qui va piano va sano"** – Une introduction en douceur pour calibrer vos réflexes.
* **"Allegro ma non troppo"** – Le rythme s'accélère, mais restez maître de votre raquette.
* **"Who switched off the lights?"** – Un défi surprenant où la visibilité ou la configuration des briques mettra vos nerfs à rude épreuve.


## 📂 Structure du projet
```text
├── assets/          # (Optionnel) Images, polices rétro et sons
├── main.py          # Point d'entrée principal du jeu
├── README.md        # Documentation du projet
└── requirements.txt # Liste des dépendances Python
```

## 📜 Licence
Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
