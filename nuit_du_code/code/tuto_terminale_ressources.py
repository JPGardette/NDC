from random import randint
import pyxel

class Vaisseau:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        """déplacement avec les touches de direction"""

        if pyxel.btn(pyxel.KEY_RIGHT):
            if (self.x < 120) :
                self.x = self.x + 1
        if pyxel.btn(pyxel.KEY_LEFT):
            if (self.x > 0) :
                self.x = self.x - 1
        if pyxel.btn(pyxel.KEY_DOWN):
            if (self.y < 120) :
                self.y = self.y + 1
        if pyxel.btn(pyxel.KEY_UP):
            if (self.y > 0) :
                self.y = self.y - 1

        if pyxel.btnr(pyxel.KEY_SPACE):
            return self.x + 4, self.y - 2

        return None

    def draw(self):

        # vaisseau (image 8x8)
        coeff= pyxel.frame_count % 4 - 1
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 0)
        pyxel.blt(self.x, self.y+8, 0, 32, 8*coeff, 8, 8, 0)

class Tir:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def is_alive(self):
        return self.alive

    def move(self):

        if self.y > 0:
            self.y = self.y - 2
        else:
            self.alive = False

    def draw(self):

        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, 0)

class Ennemi:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def is_alive(self):
        return self.alive

    def move(self):

        if self.y < 128:
            self.y = self.y + 2
        else:
            self.alive = False

    def draw(self):

        coeff = pyxel.frame_count // 3 % 3 # valeur alternant entre 1, 2 et 3 en boucle toutes les 1/10ème de seconde
        pyxel.blt(self.x, self.y, 0, 0, 8*coeff, 8, 8, 0) # la coordonnée y de l'image est donnée par  8*coeff et alterne entre 8, 16 et 24

class Explosion:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.alive = True

    def is_alive(self):
        return self.alive

    def move(self):

        if self.r<5:                # si le rayon de l'explosion ( 3ème élement ) n'a pas atteint 5 unités,
            self.r = self.r + 1     # alors on augmente ce rayon,
        else:
            self.alive = False

    def draw(self):

        pyxel.circb(self.x, self.y, self.r, 8 + (self.r)%5)

class Jeu:

    def __init__(self, h, l, titre):

        pyxel.init(h, l, title = titre)

        self.vaisseau = Vaisseau(60, 60)

        self.liste_tirs = []
        self.liste_ennemis = []
        self.liste_explosions = []

        self.score = 0
        self.vies = 5

        pyxel.load("ressources.pyxres") # chargement des ressources

        # Lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self):

        v = self.vaisseau.move()
        if v is not None:
            self.liste_tirs.append(Tir(v[0], v[1]))

        if pyxel.frame_count % 30 == 0:
            self.liste_ennemis.append(Ennemi(randint(0, 120), 0))

        for ennemi in self.liste_ennemis:
            ennemi.move()
            if not ennemi.is_alive():
                self.liste_ennemis.remove(ennemi)

        for tir in self.liste_tirs:
            tir.move()
            if not tir.is_alive():
                self.liste_tirs.remove(tir)

        for ennemi in self.liste_ennemis:
            for tir in self.liste_tirs:
                xt = tir.x
                yt = tir.y
                xe = ennemi.x
                ye = ennemi.y
                if yt <= ye+8 and ( xt >= xe and xt <= xe + 8):
                    self.liste_tirs.remove(tir)
                    self.liste_ennemis.remove(ennemi)
                    self.liste_explosions.append(Explosion(xe+4, ye+4, 1)) # ajout d'une explosion à la liste
                    self.score = self.score + 1

        for ennemi in self.liste_ennemis:
            xv = self.vaisseau.x
            yv = self.vaisseau.y
            xe = ennemi.x
            ye = ennemi.y
            if xv <= xe + 8 and xv > xe - 8 and yv <= ye + 8 and yv > ye - 8:
                self.liste_ennemis.remove(ennemi)
                self.liste_explosions.append(Explosion(xe+4, ye+4, 1)) # ajout d'une explosion à la liste
                self.vies = self.vies - 1

        for explosion in self.liste_explosions:
            explosion.move()
            if not explosion.is_alive():
                self.liste_explosions.remove(explosion)

    def draw(self):

        pyxel.cls(0)

        pyxel.bltm(0, 0, 0, 192, 192 - (pyxel.frame_count) % 192, 128, 128)

        if self.vies > 0:

            self.vaisseau.draw()

            for tir in self.liste_tirs:
                tir.draw()

            for ennemi in self.liste_ennemis:
                ennemi.draw()

            for explosion in self.liste_explosions:
                explosion.draw()

            pyxel.text(1, 1 , str(self.vies), 7)

        else:
            pyxel.text(50, 64, 'GAME OVER', 7)
            pyxel.text(50, 74, 'Score : '+ str(self.score), 7)

########################
#  PROGRAMME PRINCIPAL #
########################

Jeu(128, 128, "Super Jeu")

