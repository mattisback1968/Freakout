import sys
import pygame
import math
import random  # pour couleur de brique aléatoir, à venir

import os

from pathlib import Path
import pygame

# 1. Variable globale pour le dossier des sons
BASE_DIR = Path(__file__).resolve().parent
SOUNDS_DIR = BASE_DIR / "assets" / "sounds"
sounds_ok_ = True

# 2. Dictionnaire global pour stocker les sons chargés
SONS = {}

def charger_les_sons():
    """Initialise le mixeur et charge tous les sons du jeu en mémoire"""
    global SONS
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Liste de vos fichiers audio
        liste_sons = {
            "brique": "boing.ogg",
            "raquette": "paddle.ogg",
            "perte_vie": "lose_life.ogg",  # Futur son, vie perdue
            "victoire": "win.ogg",        # Futur son, niveau terminé
            "next": "dun_dun.ogg"  # futur son, passage au niveau supérieur
        }
        
        # Chargement automatique de chaque son
        for nom, fichier in liste_sons.items():
            chemin_complet = SOUNDS_DIR / fichier
            if chemin_complet.exists():
                SONS[nom] = pygame.mixer.Sound(str(chemin_complet))
                SONS[nom].set_volume(0.5)
            else:
                print(f"Attention : Le fichier {fichier} est introuvable.")
                SONS[nom] = None
                sound_ok = False
                
        if (sound_ok):
            print("🔊 Tous les sons ont été chargés avec succès !")
        else:
            print("🔊 Certains sons n'ont pas été chargés !")
        
    except Exception as e:
        print(f"Note : Mode audio indisponible ({e}). Mode silencieux activé.")
        # En cas de panne audio, on remplit le dictionnaire avec None pour éviter les plantages
        SONS = {"brique": None, "raquette": None, "perte_vie": None, "victoire": None, "next": None}

# Appel de la fonction au lancement du jeu


charger_les_sons()


# 1. Initialisation
pygame.init()
pygame.font.init()
police_pause = pygame.font.SysFont("Arial", 64, bold=True)
police_stats = pygame.font.SysFont("Arial", 24, bold=False)

# Initialisation du son avec sécurité anti-plantage
# . Pré-configuration et Initialisation
pygame.mixer.pre_init(44100, -16, 2, 512) # Force des paramètres audio standards et légers
pygame.init()
pygame.font.init()

# Chargement du son sécurisé
son_rebond = None
try:
    # On initialise le mixeur explicitement
    pygame.mixer.init()
    chemin_dossier = os.path.dirname(os.path.abspath(__file__))
    chemin_son = os.path.join(chemin_dossier, "boing.ogg")
    son_rebond = pygame.mixer.Sound(chemin_son)
    son_rebond = pygame.mixer.Sound("boing.ogg")
    son_rebond.set_volume(0.5)
except Exception as e:
    # Si le pilote audio ou le fichier bloque, on passe outre sans figer le programme
    print(f"Note : Mode audio indisponible ({e}). Le jeu se lance en mode silencieux.")

LARGEUR, HAUTEUR = 800, 600
ROWS = 5
COLUMNS = 8
score = 0
MAX_SCORE = ROWS * COLUMNS * 10
MAX_BRICKS = ROWS * COLUMNS
removed_bricks = 0
player = "player 1"
vies = 3
statut_jeu = "PAUSE"
level_names = ["Qui va piano va sano", "Allegro ma non troppo", "Who switched off the lights?"
               "The Real McCoy"]

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Casse-briques")

# Raquette
raquette_w, raquette_h = 100, 15
raquette_x = (LARGEUR - raquette_w) // 2
raquette_y = HAUTEUR - 40

# Balle
balle_x, balle_y = LARGEUR // 2, HAUTEUR // 2
balle_dx, balle_dy = 2, -2
balle_rayon = 10

# Définition initiale des rectangles (indispensable pour le premier rendu graphique)
rect_raquette = pygame.Rect(raquette_x, raquette_y, raquette_w, raquette_h)
rect_balle = pygame.Rect(balle_x - balle_rayon, balle_y - balle_rayon, balle_rayon * 2, balle_rayon * 2)

# Briques
briques = []
for i in range(ROWS):
    for j in range(COLUMNS):
        briques.append(pygame.Rect(j * 95 + 35, i * 35 + 50, 85, 25))

horloge = pygame.time.Clock()
en_cours = True

while en_cours:
    horloge.tick(60)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if statut_jeu == "JOUER":
                    statut_jeu = "PAUSE"
                elif statut_jeu == "PAUSE":
                    statut_jeu = "JOUER"
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


    # --- PHYSIQUE ---
    if statut_jeu == "JOUER":
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and raquette_x > 0:
            raquette_x -= 6
        if touches[pygame.K_RIGHT] and raquette_x < LARGEUR - raquette_w:
            raquette_x += 6

        balle_x += balle_dx
        balle_y += balle_dy

        # Murs et plafond
        if balle_x - balle_rayon <= 0:
            balle_x = balle_rayon
            balle_dx *= -1
        elif balle_x + balle_rayon >= LARGEUR:
            balle_x = LARGEUR - balle_rayon
            balle_dx *= -1

        if balle_y - balle_rayon <= 0:
            balle_y = balle_rayon
            balle_dy *= -1

        # Mise à jour des rectangles pour les collisions
        rect_raquette = pygame.Rect(raquette_x, raquette_y, raquette_w, raquette_h)
        rect_balle = pygame.Rect(balle_x - balle_rayon, balle_y - balle_rayon, balle_rayon * 2, balle_rayon * 2)

        # Collision Raquette (Indépendante du clavier)
        if rect_balle.colliderect(rect_raquette):
            # Sécurité physique : On recale la balle juste au-dessus de la raquette
            balle_y = raquette_y - balle_rayon

            # Déclenchement du son si disponible
            if son_rebond:
                son_rebond.play()

            # Vitesse totale voulue pour la balle (pixels par frame)
            VITESSE_TOTALE = 5.0

            # Calcul de l'impact (-1.0 à gauche, 0.0 au milieu, 1.0 à droite)
            centre_raquette = raquette_x + (raquette_w / 2)
            facteur_impact = (balle_x - centre_raquette) / (raquette_w / 2)

            # Calcul de la vitesse horizontale (limitée à 4.2 max pour éviter les trajectoires 100% horizontales)
            balle_dx = facteur_impact * 4.2

            # Ajustement magique de la vitesse verticale (Pythagore : dy = sqrt(V_totale^2 - dx^2))
            # Le max(0.1, ...) évite une valeur négative ou nulle sous la racine en cas d'arrondi
            balle_dy = -math.sqrt(
                max(0.1, VITESSE_TOTALE**2 - balle_dx**2)
            )


        # 6 Collision Briques
                # 6. Collision avec les briques
        for brique in briques[:]:
            if rect_balle.colliderect(brique):
                # On calcule le chevauchement (pénétration) sur les deux axes
                overlap_x = min(rect_balle.right, brique.right) - max(
                    rect_balle.left, brique.left
                )
                overlap_y = min(rect_balle.bottom, brique.bottom) - max(
                    rect_balle.top, brique.top
                )

                # Si le chevauchement horizontal est plus petit, le choc est latéral (côtés)
                if overlap_x < overlap_y:
                    balle_dx *= -1  # Rebond horizontal
                    # Sécurité : on recale la balle pour éviter qu'elle traverse
                    if balle_dx > 0:
                        balle_x = brique.right + balle_rayon
                    else:
                        balle_x = brique.left - balle_rayon
                # Sinon, le choc est vertical (haut ou bas)
                else:
                    balle_dy *= -1  # Rebond vertical
                    # Sécurité : on recale la balle
                    if balle_dy > 0:
                        balle_y = brique.bottom + balle_rayon
                    else:
                        balle_y = brique.top - balle_rayon

                # Logique de destruction et score
                if SONS["brique"]:
                                SONS["brique"].play()
                briques.remove(brique)
                score += 10
                removed_bricks += 1
                if removed_bricks == MAX_BRICKS:
                    statut_jeu = "VICTOIRE"
                break


        # Perte de balle
        if balle_y - balle_rayon > HAUTEUR:
            vies -= 1
            if vies <= 0:
                statut_jeu = "GAME_OVER"
            else:
                balle_x, balle_y = LARGEUR // 2, HAUTEUR // 2
                balle_dx, balle_dy = 2, -2

    # --- DESSIN ---
    ecran.fill((20, 20, 20))

    # Affichage ATH (Score et Vies)
    score_surface = police_stats.render(f"Score: {score}", True, (255, 255, 255))
    vies_surface = police_stats.render(f"Vies: {vies}", True, (255, 255, 255))
    ecran.blit(score_surface, (15, 15))
    ecran.blit(vies_surface, (LARGEUR - vies_surface.get_width() - 15, 15))

    # Dessin des éléments
    pygame.draw.rect(ecran, (255, 255, 255), rect_raquette)
    pygame.draw.circle(ecran, (255, 0, 0), (int(balle_x), int(balle_y)), balle_rayon)

    for brique in briques:
        pygame.draw.rect(ecran, (0, 128, 255), brique)

    # Écrans superposés
    if statut_jeu == "PAUSE":
        texte_surface = police_pause.render("PAUSE", True, (255, 255, 0))
        texte_rect = texte_surface.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        ecran.blit(texte_surface, texte_rect)

    elif statut_jeu == "VICTOIRE":
        texte_surface = police_pause.render(f"BRAVO {player} !", True, (0, 255, 0))
        texte_rect = texte_surface.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        ecran.blit(texte_surface, texte_rect)

    elif statut_jeu == "GAME_OVER":
        texte_surface = police_pause.render("GAME OVER", True, (255, 0, 0))
        texte_rect = texte_surface.get_rect(center=(LARGEUR // 2, HAUTEUR // 2))
        ecran.blit(texte_surface, texte_rect)

    elif statut_jeu == "MENU":
        ecran.fill((15, 15, 25))  # Fond bleu nuit très foncé
    
        # Dessin du titre principal du jeu
        texte_titre = police_pause.render("BREAKOUT ARCADIA", True, (0, 255, 255))
        rect_titre = texte_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 180))
        ecran.blit(texte_titre, rect_titre)
        
        # Récupération des coordonnées de la souris pour l'effet "Hover"
        pos_curseur = pygame.mouse.get_pos()
        
        # Bouton JOUER (Jaune si survolé, blanc sinon)
        c_jouer = (255, 255, 0) if rect_btn_jouer.collidepoint(pos_curseur) else (255, 255, 255)
        txt_jouer = police_menu.render("JOUER", True, c_jouer)
        ecran.blit(txt_jouer, txt_jouer.get_rect(center=rect_btn_jouer.center))
        
        # Bouton HALL OF FAME (Jaune si survolé, blanc sinon)
        c_scores = (255, 255, 0) if rect_btn_scores.collidepoint(pos_curseur) else (255, 255, 255)
        txt_scores = police_menu.render("HALL OF FAME", True, c_scores)
        ecran.blit(txt_scores, txt_scores.get_rect(center=rect_btn_scores.center))
        
        # Bouton QUITTER (Rouge si survolé, blanc sinon)
        c_quitter = (255, 0, 0) if rect_btn_quitter.collidepoint(pos_curseur) else (255, 255, 255)
        txt_quitter = police_menu.render("QUITTER", True, c_quitter)
        ecran.blit(txt_quitter, txt_quitter.get_rect(center=rect_btn_quitter.center))


    pygame.display.flip()

pygame.quit()
sys.exit()
