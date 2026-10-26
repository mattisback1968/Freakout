import sys
import pygame
import math

# --- IMPORTATION DE VOS MODULES FACTORISÉS ---
import config
import sound_elements  # Charge automatiquement les sons au lancement
import score_manager
import game_elements  # À activer quand les classes seront prêtes

import game_physics   # À activer pour les fonctions de collision
import screens        # dessins du menu/scores


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
player ="Killroy"

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


# Modèle de niveau simple (Vraie Matrice 2D : Liste de listes)
# 1 = Vert (1 PV), 2 = Jaune (2 PV), 3 = Rouge (3 PV)
# Ligne 0 : Verts,  # Ligne 1 : Verts,  # Ligne 2 : Jaunes,  # Ligne 3 : Jaunes   # Ligne 4 : Rouges
MATRICE_NIVEAU_1 = [[3, 3, 3, 3, 3, 3, 3, 3], [2, 2, 2, 2, 0, 2, 2, 2], [2, 2, 2, 2, 2, 0, 2, 2], [1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0]]

# Deux briques jaunes de chaque côté, du vide au centre !,  # Un trou un peu plus petit sur la ligne des vertes
MATRICE_NIVEAU_2 = [[], [], [], [], [], []]


# Fonction temporaire de génération (à déplacer dans game_elements plus tard)

def generer_mur(matrice):
    briques_creees = []
    PARAMS_BRIQUES = {
        1: {"couleur": (0, 255, 0), "vies": 1},
        2: {"couleur": (255, 255, 0), "vies": 2},
        3: {"couleur": (255, 0, 0), "vies": 3},
    }
    
    for i, ligne in enumerate(matrice):
        for j, type_brique in enumerate(ligne):
            # L'ASTUCE ICI : Si la case vaut 0, on passe directement à la brique suivante
            if type_brique == 0:
                continue
                
            if type_brique in PARAMS_BRIQUES:
                rect = pygame.Rect(j * 95 + 35, i * 35 + 60, 85, 25)
                briques_creees.append({
                    "rect": rect,
                    "couleur": PARAMS_BRIQUES[type_brique]["couleur"],
                    "vies": PARAMS_BRIQUES[type_brique]["vies"]
                })
    return briques_creees


# Génération initiale des briques
# briques = generer_mur(MATRICE_NIVEAU_1)


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
              
                briques = generer_mur(MATRICE_NIVEAU_1)
              
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
        # 1. Déplacement de la raquette
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT] and raquette_x > 0:
            raquette_x -= 6
        if touches[pygame.K_RIGHT] and raquette_x < config.LARGEUR - raquette_w:
            raquette_x += 6

        # 2. Déplacement de la balle
        balle_x += balle_dx
        balle_y += balle_dy

        # 3. Murs et plafond
        if balle_x - balle_rayon <= 0:
            balle_x = balle_rayon
            balle_dx *= -1
        elif balle_x + balle_rayon >= config.LARGEUR:
            balle_x = config.LARGEUR - balle_rayon
            balle_dx *= -1

        if balle_y - balle_rayon <= 0:
            balle_y = balle_rayon
            balle_dy *= -1

        # Mise à jour des rectangles de collision
        rect_raquette = pygame.Rect(raquette_x, raquette_y, raquette_w, raquette_h)
        rect_balle = pygame.Rect(balle_x - balle_rayon, balle_y - balle_rayon, balle_rayon * 2, balle_rayon * 2)

        # 4. Collision Raquette (Vitesse constante de 5.0 harmonisée)
        if rect_balle.colliderect(rect_raquette):
            balle_y = raquette_y - balle_rayon
            balle_dy = -abs(balle_dy)
            
            if sound_elements.SONS["raquette"]:
                sound_elements.SONS["raquette"].play()

            VITESSE_TOTALE = 5.0
            centre_raquette = raquette_x + (raquette_w / 2)
            facteur_impact = (balle_x - centre_raquette) / (raquette_w / 2)
            balle_dx = facteur_impact * 4.2
            balle_dy = -math.sqrt(max(0.1, VITESSE_TOTALE**2 - balle_dx**2))

        # 5. Collision avec les briques (Physique avancée des faces et PV)
        for brique_data in briques[:]:
            brique = brique_data["rect"]
            if rect_balle.colliderect(brique):
                if sound_elements.SONS["brique"]:
                    sound_elements.SONS["brique"].play()

                # Calcul des faces touchées
                overlap_x = min(rect_balle.right, brique.right) - max(rect_balle.left, brique.left)
                overlap_y = min(rect_balle.bottom, brique.bottom) - max(rect_balle.top, brique.top)

                if overlap_x < overlap_y:
                    balle_dx *= -1
                    balle_x = brique.right + balle_rayon if balle_dx > 0 else brique.left - balle_rayon
                else:
                    balle_dy *= -1
                    balle_y = brique.bottom + balle_rayon if balle_dy > 0 else brique.top - balle_rayon

                # Gestion des dégâts
                brique_data["vies"] -= 1
                score += 10
                
                if brique_data["vies"] <= 0:
                    briques.remove(brique_data)
                else:
                    # Dégradation visuelle de la couleur
                    if brique_data["vies"] == 2:
                        brique_data["couleur"] = (180, 100, 0)  # Orange cuite
                    elif brique_data["vies"] == 1:
                        brique_data["couleur"] = (128, 128, 128)  # Gris abîmé

                if len(briques) == 0:
                    statut_jeu = "VICTOIRE"
                    if sound_elements.SONS["victoire"]:
                        sound_elements.SONS["victoire"].play()
                break

        # 6. Perte de balle (détection avec la marche funèbre rétro)
        if balle_y - balle_rayon > config.HAUTEUR:
            vies -= 1
            if vies <= 0:
                statut_jeu = "GAME_OVER"
                if sound_elements.SONS["game_over"]:
                    sound_elements.SONS["game_over"].play()
            else:
                # Reset position pour vie suivante
                balle_x, balle_y = config.LARGEUR // 2, config.HAUTEUR // 2
                balle_dx, balle_dy = 2, -2

    elif statut_jeu == "HALL_OF_FAME":
        # Logique de calcul du scroll vertical
        scroll_y -= 1.5

    # ==========================================
    # PARTIE 3 : RENDU GRAPHIQUE (DESSIN)
    # ==========================================
    ecran.fill((20, 20, 20))  # Nettoyage de base obligatoire à chaque frame

    if statut_jeu == "MENU":
        pos_curseur = pygame.mouse.get_pos()
        screens.dessiner_menu(ecran, pos_curseur, rect_btn_jouer, rect_btn_scores, rect_btn_quitter)

    elif statut_jeu in ("JOUER", "PAUSE"):
        screens.dessiner_jeu(ecran, statut_jeu, score, vies, raquette_x, raquette_y, 
                             raquette_w, raquette_h, balle_x, balle_y, balle_rayon, briques)

    elif statut_jeu == "HALL_OF_FAME":
        # On récupère la fin du bloc de texte renvoyée par la fonction pour savoir quand reboucler
        y_fin_bloc = screens.dessiner_hall_of_fame(ecran, scroll_y, lignes_texte, ESPACEMENT_LIGNES)
        if y_fin_bloc < 0:
            scroll_y = config.HAUTEUR

    elif statut_jeu == "VICTOIRE":
        screens.dessiner_ecran_fin(ecran, "VICTOIRE", player)

    elif statut_jeu == "GAME_OVER":
        screens.dessiner_ecran_fin(ecran, "GAME_OVER", player)

    elif statut_jeu == "SAISIE_NOM":
        screens.dessiner_saisie_nom(ecran, nom_joueur, score)

    # Rafraîchissement de la fenêtre
    pygame.display.flip()


pygame.quit()
sys.exit()
