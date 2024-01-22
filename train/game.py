"""importation des bibliothèques nécessaires"""
import pygame
import pytmx
import pyscroll

"""importation de la classe player"""
from player import Player


class Game:


    def __init__(self):
        #fenetre du jeu
        self.screen = pygame.display.set_mode((1680,1050)) #création de la fenêtre
        pygame.display.set_caption("Jeu1 - loukaka")       #nom de la fenêtre

        #charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')  #importation de la carte depuis le fichier dans lequel le jeu est enrégistré
        map_data = pyscroll.data.TiledMapData(tmx_data)      #récupération des informations de la carte (informations trouvalbes sur tiled)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2      #zoom de la carte

        #création joueur
        player_position = tmx_data.get_object_by_name("player")     #la position de départ du joueur est définie sur tiled avec l'objet "player" et est importée ici
        self.player = Player(player_position.x, player_position.y)  #la position du joueur est définie

        #collisions
        """création de la liste qui contiendra les éléments qu'il est impossible de traverse"""
        self.walls = []
        """ajout des éléments impossibles à traverser dans la liste si leur nom est collision"""
        for obj in tmx_data.objects:
            if obj.name == "collision":
                self.walls.append(pygame.Rect(obj.x, obj. y, obj.width, obj.height))

        #dessiner le groupe de calques crée sur tiled
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.player)


    def handle_input(self):
        """déplacement du joueur"""
        pressed = pygame.key.get_pressed()  #récupération de la touche préssée par le joueur

        if pressed[pygame.K_UP]:
            self.player.deplacement_up()
            self.player.chang_anim('up')
        elif pressed[pygame.K_DOWN]:
            self.player.deplacement_down()
            self.player.chang_anim('down')
        elif pressed[pygame.K_LEFT]:
            self.player.deplacement_left()
            self.player.chang_anim('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.deplacement_droite()
            self.player.chang_anim('right')

    def update(self):
        self.group.update()

        #verif de la collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()
        #boucle du jeu
        run = True
        while run:
            """appel des méthodes créées nécessaire au bon fonctionnement du jeu"""
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():  #quitter le jeu
                if event.type == pygame.QUIT:
                    run = False
            clock.tick(60)  #définition du nombre de fps
        pygame.quit()