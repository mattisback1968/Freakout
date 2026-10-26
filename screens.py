import pygame
import config

# On initialise les polices localement dans le module screens
pygame.font.init()
police_menu = pygame.font.SysFont("Arial", 40, bold=True)
police_pause = pygame.font.SysFont("Arial", 64, bold=True)
police_stats = pygame.font.SysFont("Arial", 24, bold=False)

def dessiner_menu(ecran, pos_curseur, rect_btn_jouer, rect_btn_scores, rect_btn_quitter):
    """Gère le rendu visuel complet du menu principal avec l'effet Hover."""
    ecran.fill((15, 15, 25))  # Fond bleu nuit
    
    # Titre principal
    texte_titre = police_pause.render("BREAKOUT ARCADIA", True, (0, 255, 255))
    rect_titre = texte_titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2 - 180))
    ecran.blit(texte_titre, rect_titre)
    
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


def dessiner_jeu(ecran, statut_jeu, score, vies, raquette_x, raquette_y, raquette_w, raquette_h, balle_x, balle_y, balle_rayon, briques):
    """Gère le rendu de la partie en cours (Balle, Raquette, Briques, HUD) et de la Pause."""
    # Affichage du HUD (Score et Vies)
    score_surface = police_stats.render(f"Score: {score}", True, (255, 255, 255))
    vies_surface = police_stats.render(f"Vies: {vies}", True, (255, 255, 255))
    ecran.blit(score_surface, (15, 15))
    ecran.blit(vies_surface, (config.LARGEUR - vies_surface.get_width() - 15, 15))

    # Dessin des entités
    pygame.draw.rect(ecran, (255, 255, 255), pygame.Rect(raquette_x, raquette_y, raquette_w, raquette_h))
    pygame.draw.circle(ecran, (255, 0, 0), (int(balle_x), int(balle_y)), balle_rayon)

    # Dessin du mur
    for brique_data in briques:
        pygame.draw.rect(ecran, brique_data["couleur"], brique_data["rect"])

    # Superposition de la pause si nécessaire
    if statut_jeu == "PAUSE":
        texte_surface = police_pause.render("PAUSE", True, (255, 255, 0))
        texte_rect = texte_surface.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2))
        ecran.blit(texte_surface, texte_rect)


def dessiner_saisie_nom(ecran, nom_actuel, score_final):
    """Affiche l'écran permettant au joueur de taper ses 5 lettres."""
    ecran.fill((15, 15, 25)) # Fond bleu nuit
    
    # 1. Message principal
    txt_titre = police_menu.render("NOUVEAU HIGH SCORE !", True, (255, 255, 0))
    ecran.blit(txt_titre, txt_titre.get_rect(center=(config.LARGEUR // 2, 150)))
    
    # 2. Rappel du score
    txt_score = police_stats.render(f"Votre score : {score_final} PTS", True, (255, 255, 255))
    ecran.blit(txt_score, txt_score.get_rect(center=(config.LARGEUR // 2, 220)))
    
    # 3. Affichage des lettres en cours de saisie
    # On affiche des tirets si le joueur n'a pas encore écrit les 3 lettres
    affichage_nom = nom_actuel + "_" * (5 - len(nom_actuel))
    txt_nom = police_pause.render(affichage_nom, True, (0, 255, 255))
    ecran.blit(txt_nom, txt_nom.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2)))
    
    # 4. Instruction
    txt_info = police_stats.render("Tapez entre 3 et 5 lettres puis appuyez sur ENTRÉE", True, (128, 128, 128))
    ecran.blit(txt_info, txt_info.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR - 150)))



def dessiner_hall_of_fame(ecran, scroll_y, lignes_texte, espacement_lignes):
    """Gère le rendu des lignes défilantes du Hall of Fame."""
    ecran.fill((20, 20, 20))  # Fond sombre
    
    y_actuel = scroll_y
    for surface in lignes_texte:
        x_centre = (config.LARGEUR - surface.get_width()) // 2
        
        if -50 < y_actuel < config.HAUTEUR + 50:
            ecran.blit(surface, (x_centre, y_actuel))
            
        y_actuel += espacement_lignes
    
    return y_actuel  # On retourne la position de la dernière ligne pour le rebouclage dans le main


def dessiner_ecran_fin(ecran, type_fin, nom_joueur):
    """Affiche l'écran de Victoire ou de Game Over."""
    ecran.fill((10, 10, 10))
    
    if type_fin == "VICTOIRE":
        texte = police_pause.render(f"BRAVO {nom_joueur} !", True, (0, 255, 0))
    else:
        texte = police_pause.render("GAME OVER", True, (255, 0, 0))
        
    rect_texte = texte.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2))
    ecran.blit(texte, rect_texte)
