import pygame
from pathlib import Path

# 1. Configuration des chemins avec Pathlib (Universel)
BASE_DIR = Path(__file__).resolve().parent
# Si sound_elements.py est à la racine, son chemin sera : racine/assets/sounds
SOUNDS_DIR = BASE_DIR / "assets" / "sounds"

# 2. Dictionnaire global accessible depuis le main
SONS = {}
sounds_ok = True

def charger_les_sons():
    """Initialise le mixeur et charge tous les sons du jeu en mémoire."""
    global SONS, sounds_ok
    
    # Pré-configuration pour éviter le gel du Raspberry Pi / Linux
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            
        liste_sons = {
            "brique": "boing.ogg",
            "raquette": "paddle.ogg",
            "perte_vie": "lose_life.ogg",  
            "victoire": "win.ogg",        
            "next": "dun_dun.ogg"  
        }
        
        for nom, fichier in liste_sons.items():
            chemin_complet = SOUNDS_DIR / fichier
            
            if chemin_complet.exists():
                SONS[nom] = pygame.mixer.Sound(str(chemin_complet))
                SONS[nom].set_volume(0.5)
            else:
                print(f"⚠️ Fichier introuvable : {chemin_complet}")
                SONS[nom] = None
                sounds_ok = False
                
        if sounds_ok:
            print("🔊 Tous les sons ont été chargés avec succès depuis /assets/sounds/ !")
        else:
            print("📻 Certains sons sont manquants, mode partiel activé.")
        
    except Exception as e:
        print(f"❌ Mode audio indisponible ({e}). Mode silencieux activé.")
        # Remplissage par défaut pour éviter les NameError dans le main
        SONS = {
            "brique": None, "raquette": None, "perte_vie": None, 
            "victoire": None, "next": None
        }
        sounds_ok = False

# Exécution automatique lors de l'importation du module


charger_les_sons()
