import sys
import pygame

# --- IMPORTATION DE VOS MODULES FACTORISÉS ---
import config
import sound_elements  # Charge automatiquement les sons au lancement
import score_manager
import game_elements  # À activer quand vos classes seront prêtes

import game_physics   # À activer pour les fonctions de collision
import screens        # À activer pour déporter les dessins du menu/scores


# 1. INITIALISATION GLOBALE VIA CONFIG
pygame.init()
pygame.font.init()

ecran = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR))
pygame.display.set_caption("BREAKOUT ARCADIA")
horloge = pygame.time.Clock()

# Polices globales
police_pause = pygame.font.SysFont("Arial", 64, bold=True)
police_stats = pygame.font.SysFont("Arial", 24, bold=False)

# Variables d'état initiales
statut_jeu = "MENU"  # "MENU", "JOUER", "PAUSE", "VICTOIRE", "GAME_OVER", "HALL_OF_FAME"
vies = 3
score = 0
en_cours = True

# --- INITIALISATION TEMPORAIRE DES ÉLÉMENTS (En attendant game_elements.py) ---
raquette_w, raquette_h = 100, 15
raquette_x = (config.LARGEUR - raquette_w) // 2
raquette_y = config.HAUTEUR - 40
balle_x, balle_y = config.LARGEUR // 2, config.HAUTEUR // 2
balle_dx, balle_dy = 2, -2
balle_rayon = 10
briques = []  # boucle de création de briques vient ici

# Variable pour le scroll du Hall of Fame
scroll_y = config.HAUTEUR

# Police pour les boutons
police_menu = pygame.font.SysFont("Arial", 40, bold=True)

# Zones de clic virtuelles centrées à l'écran
rect_btn_jouer = pygame.Rect(0, 0, 200, 50)
rect_btn_jouer.center = (config.LARGEUR // 2, config.HAUTEUR // 2 - 60)

rect_btn_scores = pygame.Rect(0, 0, 300, 50)
rect_btn_scores.center = (config.LARGEUR // 2, config.HAUTEUR // 2 + 10)

rect_btn_quitter = pygame.Rect(0, 0, 200, 50)
rect_btn_quitter.center = (config.LARGEUR // 2, config.HAUTEUR // 2 + 80)

# --- INITIALISATION DE L'ÉCRAN HALL OF FAME ---
# Chargement des scores depuis votre manager JSON
les_scores = score_manager.charger_scores()

# Liste qui va stocker les surfaces de texte Pygame
police_hof = pygame.font.SysFont("Arial", 32, bold=True)
lignes_texte = []

# Titre propre en pur ASCII pour éviter le bug du carré/tofu
lignes_texte.append(police_hof.render("=== * HALL OF FAME * ===", True, (255, 255, 0)))
lignes_texte.append(police_hof.render("-------------------", True, (255, 255, 255)))

# Remplissage automatique avec les données du JSON
for rang, donnees in enumerate(les_scores, start=1):
    texte_ligne = f"{rang}. {donnees['name']} : {donnees['score']} PTS"
    surface_ligne = police_hof.render(texte_ligne, True, (255, 255, 255))
    lignes_texte.append(surface_ligne)

# Variables pour le défilement (scroll)
scroll_y = config.HAUTEUR  # Le texte commence en bas de l'écran
vitesse_defilement = 1.5   # Vitesse de la montée
ESPACEMENT_LIGNES = 45     # Écart en pixels entre chaque ligne


# 2. BOUCLE PRINCIPALE (AIGUILLAGE)
while en_cours:
    horloge.tick(config.FPS)

    # ==========================================
    # PARTIE 1 : GESTION DES ÉVÉNEMENTS
    # ==========================================
    evenements = pygame.event.get()
    for event in evenements:
        if event.type == pygame.QUIT:
            en_cours = False

        # Échap quitte le jeu depuis le menu, ou revient au menu depuis les scores
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if statut_jeu == "MENU":
                en_cours = False
            elif statut_jeu in ("HALL_OF_FAME", "VICTOIRE", "GAME_OVER"):
                statut_jeu = "MENU"

        # Touche Espace -> pause
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
            and statut_jeu in ("JOUER", "PAUSE")
        ):
            statut_jeu = "PAUSE" if statut_jeu == "JOUER" else "JOUER"

    # Aiguillage des événements spécifiques selon l'écran
    if statut_jeu == "MENU":
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 = Clic gauche
            pos_souris = event.pos
          
            if rect_btn_jouer.collidepoint(pos_souris):
                # Réinitialisation des variables de jeu
                score = 0
                vies = 3
                removed_bricks = 0
                balle_x, balle_y = config.LARGEUR // 2, config.HAUTEUR // 2
                balle_dx, balle_dy = 2, -2
              
              # C'est ici qu'on appellera la fonction pour reconstruire le mur de briques
              # ex: briques = game_elements.creer_mur()
              
                statut_jeu = "JOUER"
              
            elif rect_btn_scores.collidepoint(pos_souris):
                scroll_y = config.HAUTEUR # Reset du scroll en bas de l'écran
                statut_jeu = "HALL_OF_FAME"
              
            elif rect_btn_quitter.collidepoint(pos_souris):
                en_cours = False


    # ==========================================
    # PARTIE 2 : PHYSIQUE ET LOGIQUE
    # ==========================================
    if statut_jeu == "JOUER":
        # Insérer ici l'appel à la logique de déplacement et collisions
        # Plus tard, ce sera simplement : game_physics.calculer_collisions(...)
        pass
    elif statut_jeu == "HALL_OF_FAME":
        # Logique de calcul du scroll vertical
        scroll_y -= 1.5

    # ==========================================
    # PARTIE 3 : RENDU GRAPHIQUE (DESSIN)
    # ==========================================
    ecran.fill((20, 20, 20))  # On efface toujours avec le fond de base

    # Aiguillage des événements spécifiques selon l'écran
    if statut_jeu == "MENU":
        ecran.fill((15, 15, 25))  # Fond bleu nuit très foncé
      
        # Affichage du titre principal
        texte_titre = police_pause.render("FREAKOUT ARCADIA", True, (0, 255, 255))
        rect_titre = texte_titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2 - 180)) # Correction de la typo texte_titre -> text_titre si besoin, restons sur texte_titre
        rect_titre = texte_titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2 - 180))
        ecran.blit(texte_titre, rect_titre)
      
        # Récupération de la position du curseur PC
        pos_curseur = pygame.mouse.get_pos()
      
        # Bouton JOUER
        c_jouer = (255, 255, 0) if rect_btn_jouer.collidepoint(pos_curseur) else (255, 255, 255)
        txt_jouer = police_menu.render("JOUER", True, c_jouer)
        ecran.blit(txt_jouer, txt_jouer.get_rect(center=rect_btn_jouer.center))
      
        # Bouton HALL OF FAME
        c_scores = (255, 255, 0) if rect_btn_scores.collidepoint(pos_curseur) else (255, 255, 255)
        txt_scores = police_menu.render("HALL OF FAME", True, c_scores)
        ecran.blit(txt_scores, txt_scores.get_rect(center=rect_btn_scores.center))
      
        # Bouton QUITTER
        c_quitter = (255, 0, 0) if rect_btn_quitter.collidepoint(pos_curseur) else (255, 255, 255)
        txt_quitter = police_menu.render("QUITTER", True, c_quitter)
        ecran.blit(txt_quitter, txt_quitter.get_rect(center=rect_btn_quitter.center))

    elif statut_jeu == "JOUER" or statut_jeu == "PAUSE":
        # Dessin du HUD, de la raquette, de la balle et des briques
        # Si statut_jeu == "PAUSE", on blit le texte "PAUSE" par-dessus
        pass

    elif statut_jeu == "VICTOIRE":
        # Affichage de l'écran de victoire
        pass

    elif statut_jeu == "HALL_OF_FAME":
        # On garde le fond sombre de base
        ecran.fill((20, 20, 20))
        
        # Position de départ pour la première ligne
        y_actuel = scroll_y
        
        for surface in lignes_texte:
            # Centrage horizontal automatique de chaque ligne de score
            x_centre = (config.LARGEUR - surface.get_width()) // 2
            
            # Optimisation : On ne dessine que si la ligne est visible
            if -50 < y_actuel < config.HAUTEUR + 50:
                ecran.blit(surface, (x_centre, y_actuel))
                
            # On décale le Y pour la ligne suivante
            y_actuel += ESPACEMENT_LIGNES
            
        # LE REBOUCLAGE : Si 'y_actuel' (la fin de la dernière ligne) passe au-dessus de l'écran
        if y_actuel < 0:
            scroll_y = config.HAUTEUR  # Le défilement repart du bas


    # Rafraîchissement de l'écran
    pygame.display.flip()

pygame.quit()
sys.exit()
