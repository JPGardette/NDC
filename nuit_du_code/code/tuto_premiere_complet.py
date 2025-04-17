from random import randint
import pyxel

pyxel.init(128, 128, title="Super Jeu")

###############################
# FONCTIONS GÉRANT LE VAISSEAU #
###############################

def bouge_vaisseau():

    global vaisseau_x, vaisseau_y # Variables globales modifiées dans cette fonction

    # déplacement du vaisseau
    if pyxel.btn(pyxel.KEY_RIGHT):
        if (vaisseau_x < 120) :
            vaisseau_x = vaisseau_x + 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (vaisseau_x > 0) :
            vaisseau_x = vaisseau_x - 1
    if pyxel.btn(pyxel.KEY_DOWN):
        if (vaisseau_y < 120) :
            vaisseau_y = vaisseau_y + 1
    if pyxel.btn(pyxel.KEY_UP):
        if (vaisseau_y > 0) :
            vaisseau_y = vaisseau_y - 1

    if pyxel.btnr(pyxel.KEY_SPACE):                             # si la touche "ESPACE" a été appuyée :
        liste_tirs.append([vaisseau_x + 4, vaisseau_y - 2])     # on ajoute à la liste 'liste_tirs' un nouveau tir


def affiche_vaisseau():

    # vaisseau (carre 8x8)
    pyxel.rect(vaisseau_x, vaisseau_y, 8, 8, 1)

###########################
# FONCTIONS GÉRANT LE TIR #
###########################

def bouge_tir(tir):

    if tir[1]>0:                # si il n'a pas atteint le haut de l'écran,
        tir[1] = tir[1] - 2     # alors on le déplace,
    else:
        liste_tirs.remove(tir)  # sinon on le supprime de la liste

def affiche_tir(tir):

    pyxel.rect(tir[0], tir[1], 1, 4, 10)

################################
# FONCTIONS GÉRANT LES ENNEMIS #
################################

def bouge_ennemi(ennemi):

    if ennemi[1]<128:                # si il n'a pas atteint le bas de l'écran,
        ennemi[1] = ennemi[1] + 2     # alors on le déplace,
    else:
        liste_ennemis.remove(ennemi)  # sinon on le supprime de la liste

def affiche_ennemi(ennemi):

    pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

###################################
# FONCTIONS GÉRANT LES EXPLOSIONS #
###################################

def bouge_explosion(explosion):

    if explosion[2]<5:                      # si le rayon de l'explosion ( 3ème élement ) n'a pas atteint 5 unités,
        explosion[2] = explosion[2] + 1     # alors on augmente ce rayon,
    else:
        liste_explosions.remove(explosion)  # sinon l'explosion est terminée, on la supprime de la liste

def affiche_explosion(explosion):

    pyxel.circb(explosion[0], explosion[1], explosion[2], 8+explosion[2]%5)  # cercles de rayon croissant et de couleur variable !

##################
# GESTION DU JEU #
##################

def update():

    global score, vies

    bouge_vaisseau()

    # Déplacement des tirs
    for tir in liste_tirs:
        bouge_tir(tir)

    # Création des ennemis toutes les 30 frames = 1 s
    if pyxel.frame_count % 30 == 0:
        liste_ennemis.append([randint(0, 120), 0])

    # Déplacement des ennemis
    for ennemi in liste_ennemis:
        bouge_ennemi(ennemi)

    # Détection collisions ennemis/tirs
    for ennemi in liste_ennemis:
        for tir in liste_tirs:
            xt = tir[0]
            yt = tir[1]
            xe = ennemi[0]
            ye = ennemi[1]
            if yt <= ye+8 and ( xt >= xe and xt <= xe + 8): # si les conditions de collisions sont vérifiées,
                liste_tirs.remove(tir)                      # on supprime le tir de sa liste,
                liste_ennemis.remove(ennemi)                # idem pour l'ennemi,
                liste_explosions.append([xe+4, ye+4, 1])    # et on ajoute une explosion à la liste ( rayon initial = 1 unité )
                score = score + 1

    for ennemi in liste_ennemis:
        xv = vaisseau_x
        yv = vaisseau_y
        xe = ennemi[0]
        ye = ennemi[1]
        if xv <= xe + 8 and xv > xe - 8 and yv <= ye + 8 and yv > ye - 8:
            liste_ennemis.remove(ennemi)
            liste_explosions.append([xe+4, ye+4, 1]) # ajout d'une explosion à la liste
            vies = vies - 1

    for explosion in liste_explosions:
        bouge_explosion(explosion)

def draw():

    pyxel.cls(0)

    if vies > 0:
        affiche_vaisseau()

        for tir in liste_tirs:
            affiche_tir(tir)

        for ennemi in liste_ennemis:
            affiche_ennemi(ennemi)

        for explosion in liste_explosions:
            affiche_explosion(explosion)

        pyxel.text(1, 1 , str(vies), 7)

    else:
        pyxel.text(50, 64, 'GAME OVER', 7)
        pyxel.text(50, 74, 'Score : '+ str(score), 7)

########################
#  PROGRAMME PRINCIPAL #
########################

# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60

liste_tirs = [] # liste des tirs
liste_ennemis = [] # liste des ennemis
liste_explosions = []

score = 0
vies = 5

# Lancement du jeu
pyxel.run(update, draw)
