import pygame
import pytmx


class Player(pygame.sprite.Sprite):

    def __init__(self, x , y):
        super().__init__() #appel de la classe super pour certaines méthodes de pygame
        self.sprite_sheet = pygame.image.load('player.png')  #sélection des image du joueur dans les fichiers locaux
        self.image = self.get_image(0, 0)  #sélection de l'image de base du joueur
        self.image.set_colorkey(0, 0)  #contour du joueur en transparent
        self.rect = self.image.get_rect()  #création d'un rectangle autour du joueur
        self.position = [x, y] #variable qui définit la postion du joueur
        self.images = {
            'down' : self.get_image(0, 0),
            'left' : self.get_image(0, 32),       #dictionnaire qui contient les images nécessaire selon le direction du joueur
            'up' : self.get_image(0, 96),
            'right': self.get_image(0, 64)
        }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)  #création d'un rectangle au niveau des pieds du joueur pour les collisions
        self.old_position = self.position.copy()  #
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        self.speed = 3




    def save_location(self):
        self.old_position = self.position.copy()

    def chang_anim(self, name):
        """changement de la position du joueur selon la direction de déplacement """
        self.image = self.images[name]
        self.image.set_colorkey(0, 0)

    def deplacement_droite(self):
        self.position[0] += self.speed

    def deplacement_left(self):
        self.position[0] -= self.speed
                                                    #Définition de la nouvelle position du joueur après déplacement
    def deplacement_up(self):
        self.position[1] -= self.speed

    def deplacement_down(self):
        self.position[1] += self.speed


    def update(self):
        self.rect.topleft = self.position               #mise à jour du déplacement
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position
        self.rect.topleft = self.position               #nouvelle position en cas de collision
        self.feet.midbottom = self.rect.midbottom


    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0,0), (x, y ,32 ,32))
        return image
