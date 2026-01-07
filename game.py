import pygame
import pytmx
import pyscroll
from player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("MMORPG Proto - GTA 7 style")

        # Chargement carte Tiled
        tmx_data = pytmx.util_pygame.load_pygame("asset/mapes/mape.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2  # Optionnel : zoom pour mieux voir

        # Collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Spawn joueur
        player_obj = tmx_data.get_object_by_name("player")
        self.player = Player(player_obj.x, player_obj.y)

        # Groupe rendu
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        dx = dy = 0

        if pressed[pygame.K_UP]:
            dy -= 1
            self.player.direction = 'up'
        if pressed[pygame.K_DOWN]:
            dy += 1
            self.player.direction = 'down'
        if pressed[pygame.K_LEFT]:
            dx -= 1
            self.player.direction = 'left'
        if pressed[pygame.K_RIGHT]:
            dx += 1
            self.player.direction = 'right'

        if dx != 0 or dy != 0:
            self.player.moving = True
            # Normalisation diagonale (optionnel, sinon vitesse x1.4)
            if dx != 0 and dy != 0:
                dx /= 1.414  # ≈√2
                dy /= 1.414

            self.player.move(dx, dy)

    def update(self):
        self.player.update()        # <-- Important : on l'avait oublié !
        self.group.update()

        # Collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack()

            clock.tick(60)

        pygame.quit()
