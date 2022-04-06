import pygame
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

#Titre de la fenêtre
pygame.display.set_caption("Jeu du Pong")

#Ouverture de la fenêtre Pygame
taille = largeur, hauteur = 1200, 600
fenetre = pygame.display.set_mode(taille)

#gestion de la musique de fond
pygame.mixer.music.load('musique.wav')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(fade_ms=15000, loops=15)

#variable couleur
BLUE = pygame.Color(0,0,255)

#fonction création d'un menu
def menu():
    continuer=True
    bouton = pygame.image.load("boutonplay.png").convert()
    boutonrect = bouton.get_rect()
    boutonrect.centerx,boutonrect.centery=largeur/2, hauteur/2

    while continuer:
        fenetre.fill((0,0,0))
        font = pygame.font.Font(None, 80)
        text = font.render("Press Space to start", 1, (0, 0, 255))
        textpos = text.get_rect()
        textpos.centerx, textpos.centery=largeur/2, hauteur/2+180

        fenetre.blit(bouton,boutonrect)
        fenetre.blit(text,textpos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    continuer=False
                    jeu()

#création d'un menu de fin
def menudefin():
    continuer=True

    while continuer:
        fenetre.fill((0,0,0))
        font = pygame.font.Font(None, 48)
        text = font.render("Press enter to restart or Press space to quit", 1, (0, 0, 255))
        textpos = text.get_rect()
        textpos.centerx, textpos.centery=largeur/2, hauteur/2+10

        fenetre.blit(text,textpos)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    continuer=False
                    menu()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    continuer=False

def jeu():

    #liste
    listevitesse=[5,-5]

    #Chargement et collage de la balle
    balle = pygame.image.load("ball.png").convert()
    ballerect = balle.get_rect()
    ballerect.x,ballerect.y=largeur/2, hauteur/2

    #configuration de la barre gauche
    barre_gauche = pygame.image.load("barre.png").convert()
    barrerect_gauche = barre_gauche.get_rect()
    barrerect_gauche.centery=hauteur/2
    barrerect_gauche.x=15

    #configuration de la barre droite
    barre_droite = pygame.image.load("barre.png").convert()
    barrerect_droite = barre_droite.get_rect()
    barrerect_droite.x=largeur-30
    barrerect_droite.centery=hauteur/2

    #Création des variables
    font = pygame.font.Font(None, 80)
    vitesse = [3,3]
    noir = 0, 0, 0
    continuer = 1
    score_g=0
    score_d=0

    pygame.key.set_repeat(10,30)

    while continuer:

        #Création de la boucle de déplacement de la balle
        pygame.time.Clock().tick(100) #pour ralentir la boucle de jeu
        ballerect = ballerect.move(vitesse)

        if ballerect.left < 0 : # changement de direction de la balle si atteint les bords gauche ou droit
            ballerect.x,ballerect.y=largeur/2, hauteur/2
            score_d+=1
            vitesse[0]=listevitesse[randint(0,1)]
            vitesse[1]=listevitesse[randint(0,1)]

        if ballerect.right > largeur:
            ballerect.x,ballerect.y=largeur/2, hauteur/2
            score_g+=1
            vitesse[0]=listevitesse[randint(0,1)]
            vitesse[1]=listevitesse[randint(0,1)]


        if ballerect.top < 0 or ballerect.bottom > hauteur: # changement de direction de la balle si atteint les bords bas ou haut
             vitesse[1] = -vitesse[1]

        #collision des barres
        if ballerect.colliderect(barrerect_gauche):
            vitesse[0]=-vitesse[0]

        if barrerect_gauche.top<0:
            barrerect_gauche.y=0

        if barrerect_gauche.bottom>hauteur:
            barrerect_gauche.y=hauteur-69

        if ballerect.colliderect(barrerect_droite):
             vitesse[0]=-vitesse[0]

        if barrerect_droite.top<0:
            barrerect_droite.y=0

        if barrerect_droite.bottom>hauteur:
            barrerect_droite.y=hauteur-69

        #Arrête le jeu si 1 joueur atteind 10 points
        if score_d == 3 or score_g == 3:
            continuer=False
            menudefin()

        #Gestion de la fermeture :
        for event in pygame.event.get():   #On parcourt la liste de tous les événements reçus

            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
                
            #mouvement de la barre de gauche:
            if event.type == KEYDOWN:
                if event.key == K_DOWN: #Si "flèche bas"
                    barrerect_droite = barrerect_droite.move(0,10) #On descend la barre de gauche de 10 pixels

            if event.type == KEYDOWN:
                if event.key == K_UP:   #Si "flèche haut"
                    barrerect_droite = barrerect_droite.move(0,-10) #On monte la barre de gauche de 10 pixels

            #mouvement de la barre de droite:
            if event.type == KEYDOWN:
                if event.key == K_s: #Si "s"
                    barrerect_gauche = barrerect_gauche.move(0,10) #On descend la barre de gauche de 10 pixels

            if event.type == KEYDOWN:
                if event.key == K_z:   #Si "z"
                    barrerect_gauche = barrerect_gauche.move(0,-10) #On monte la barre de gauche de 10 pixels

        fenetre.fill(noir)  #Remplissage de l'écran
        
        #Création de la ligne de séparation centrale
        pygame.draw.rect(fenetre,BLUE,pygame.Rect(600,0,5,800)) 

        #dessin de la balle
        fenetre.blit(balle, ballerect)

        #dessin des barres
        fenetre.blit(barre_gauche, barrerect_gauche)
        fenetre.blit(barre_droite, barrerect_droite)
        
        #affichage du score joueur 1
        text = font.render(str(score_g), 1, (255, 255, 0))
        textpos = text.get_rect()
        fenetre.blit(text,(160,10))
        
        #affichage du score joueur 2
        text = font.render(str(score_d), 1, (255, 255, 0))
        textpos = text.get_rect()
        fenetre.blit(text,(largeur-190,10))

        #Rafraîchissement de l'écran
        pygame.display.update()
menu()

pygame.quit()

