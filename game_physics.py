import pygame
from config import LARGEUR, HAUTEUR

def gerer_collisions_murs(balle, sons):
    """
    Gère les rebonds de la balle sur les bordures de l'écran (gauche, droite, haut).
    Retourne True si la balle est perdue par le bas, False sinon.
    """
    # Mur Gauche
    if balle.rect.left <= 0:
        balle.rect.left = 0
        balle.vx *= -1
        if sons.get("rebond"):
            sons["rebond"].play()

    # Mur Droit
    elif balle.rect.right >= WIDTH:
        balle.rect.right = WIDTH
        balle.vx *= -1
        if sons.get("rebond"): 
            sons["rebond"].play()

    # Plafond (Haut)
    if balle.rect.top <= 0:
        balle.rect.top = 0
        balle.vy *= -1
        if sons.get("rebond"): 
            sons["rebond"].play()

    # Sortie par le bas (Perte de bille)
    if balle.rect.bottom >= HEIGHT:
        return True
        
    return False


def gerer_collision_raquette(balle, raquette, sons):
    """
    Gère la collision entre la balle et la raquette avec repositionnement de sécurité
    et calcul de l'angle directionnel selon le point d'impact.
    """
    if balle.rect.colliderect(raquette.rect):
        # Sécurité : On s'assure que la balle descend bien pour éviter les doubles collisions
        if balle.vy > 0:
            # 1. Repositionnement sur le dessus de la raquette
            balle.rect.bottom = raquette.rect.top
            
            # 2. Calcul du rebond directionnel (style arcade)
            # Distance entre le centre de la raquette et le centre de la balle
            centre_raquette = raquette.rect.centerx
            centre_balle = balle.rect.centerx
            relative_x = centre_balle - centre_raquette
            
            # Facteur d'inclinaison (-1.0 à gauche, 0.0 au centre, 1.0 à droite)
            facteur_angle = relative_x / (raquette.rect.width / 2)
            
            # Limitation du facteur (au cas où la balle tape l'extrême bordure)
            facteur_angle = max(-1.0, min(1.0, facteur_angle))
            
            # Ajustement des vitesses (on garde une vitesse globale cohérente)
            vitesse_totale = 7 # Vitesse de référence de la balle
            balle.vx = facteur_angle * vitesse_totale
            
            # Rebond vers le haut (vy toujours négatif)
            # Utilisation de la racine carrée pour maintenir une vitesse globale stable (Pythagore)
            import math
            balle.vy = -math.sqrt(max(4, vitesse_totale**2 - balle.vx**2))
            
            # Déclenchement du son de la raquette
            if sons.get("rebond_raquette"):
                sons["rebond_raquette"].play()
            elif sons.get("rebond"):
                sons["rebond"].play()


def gerer_collisions_briques(balle, liste_briques, score_actuel, sons):
    """
    Gère l'impact de la balle sur les briques du niveau avec détection fine des côtés.
    """
    briques_touchees = []
    for brique in liste_briques:
        if balle.rect.colliderect(brique):
            briques_touchees.append(brique)

    if not briques_touchees:
        return score_actuel

    for brique in briques_touchees:
        # Calcul du chevauchement (overlap)
        overlap_x = min(balle.rect.right, brique.right) - max(balle.rect.left, brique.left)
        overlap_y = min(balle.rect.bottom, brique.bottom) - max(balle.rect.top, brique.top)

        if overlap_x < overlap_y:
            # Collision latérale (gauche / droite)
            balle.vx *= -1
            if balle.vx > 0:
                balle.rect.left = brique.right
            else:
                balle.rect.right = brique.left
        else:
            # Collision verticale (haut / bas)
            balle.vy *= -1
            if balle.vy > 0:
                balle.rect.top = brique.bottom
            else:
                balle.rect.bottom = brique.top

        # Conséquences du choc
        liste_briques.remove(brique)
        score_actuel += 10
        
        if sons.get("brique"):
            sons["brique"].play()

    return score_actuel
