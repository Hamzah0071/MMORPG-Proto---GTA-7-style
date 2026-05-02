import pygame
import pytmx
import pyscroll
from player import Player
from slime import Slime

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GTA Slime - Proto")
        
        # Police pour l'interface
        self.font = pygame.font.SysFont("Arial", 24, bold=True)

        # Chargement carte Tiled
        tmx_data = pytmx.util_pygame.load_pygame("asset/mapes/mape.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Collisions
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Spawn joueur
        player_obj = tmx_data.get_object_by_name("player")
        self.player = Player(player_obj.x, player_obj.y)

        # Liste des ennemis
        self.enemies = pygame.sprite.Group()
        # On ajoute quelques slimes autour du joueur pour tester
        for i in range(3):
            self.enemies.add(Slime(player_obj.x + 100 + (i*50), player_obj.y + 100))

        # Groupe rendu
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
        for enemy in self.enemies:
            self.group.add(enemy)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        dx = dy = 0

        if pressed[pygame.K_UP] or pressed[pygame.K_z]:
            dy -= 1
            self.player.direction = 'up'
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            dy += 1
            self.player.direction = 'down'
        if pressed[pygame.K_LEFT] or pressed[pygame.K_q]:
            dx -= 1
            self.player.direction = 'left'
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            dx += 1
            self.player.direction = 'right'

        if dx != 0 or dy != 0:
            self.player.moving = True
            if dx != 0 and dy != 0:
                dx /= 1.414
                dy /= 1.414
            self.player.move(dx, dy)

    def update(self):
        self.player.update()
        self.enemies.update()
        self.group.update()

        # Collisions murs
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

        # Combat : Si le joueur attaque et touche un ennemi
        if self.player.is_attacking:
            # On crée un rect d'attaque devant le joueur
            attack_rect = self.player.rect.copy()
            if self.player.direction == 'up': attack_rect.y -= 20
            elif self.player.direction == 'down': attack_rect.y += 20
            elif self.player.direction == 'left': attack_rect.x -= 20
            elif self.player.direction == 'right': attack_rect.x += 20
            
            for enemy in self.enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.kill()

        # Dégâts au joueur si contact avec un slime
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.health -= 0.1 # Dégâts continus légers
                if self.player.health < 0: self.player.health = 0

    def draw_ui(self):
        bar_width = 200
        bar_height = 20
        x, y = 20, 20
        
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))
        health_width = (self.player.health / self.player.max_health) * bar_width
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, health_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        health_text = self.font.render(f"PV: {int(self.player.health)}", True, (255, 255, 255))
        self.screen.blit(health_text, (x, y + 25))

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.player.save_location()
            for enemy in self.enemies:
                enemy.save_location()
                
            self.handle_input()
            self.update()
            
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.draw_ui()
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.attack()

            clock.tick(60)

        pygame.quit()
