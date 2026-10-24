import pygame

def dessiner_menu():
    

        # Dessin du titre principal
        texte_titre = police_pause.render(
            "BREAKOUT ARCADIA", True, (0, 255, 255)
        )
        rect_titre = texte_titre.get_rect(
            center=(LARGEUR // 2, HAUTEUR // 2 - 180)
        )
        ecran.blit(texte_titre, rect_titre)

        # Récupération des coordonnées de la souris pour l'effet "Hover"
        pos_curseur = pygame.mouse.get_pos()

        # Bouton JOUER
        c_jouer = (
            (255, 255, 0)
            if rect_btn_jouer.collidepoint(pos_curseur)
            else (255, 255, 255)
        )
        txt_jouer = police_menu.render("JOUER", True, c_jouer)
        ecran.blit(txt_jouer, txt_jouer.get_rect(center=rect_btn_jouer.center))

        # Bouton HALL OF FAME
        c_scores = (
            (255, 255, 0)
            if rect_btn_scores.collidepoint(pos_curseur)
            else (255, 255, 255)
        )
        txt_scores = police_menu.render("HALL OF FAME", True, c_scores)
        ecran.blit(
            txt_scores, txt_scores.get_rect(center=rect_btn_scores.center)
        )

        # Bouton QUITTER
        c_quitter = (
            (255, 0, 0)
            if rect_btn_quitter.collidepoint(pos_curseur)
            else (255, 255, 255)
        )
        txt_quitter = police_menu.render("QUITTER", True, c_quitter)
        ecran.blit(
            txt_quitter, txt_quitter.get_rect(center=rect_btn_quitter.center)
        )

    # MISE À JOUR ESSENTIELLE DE L'ÉCRAN
        pygame.display.flip()