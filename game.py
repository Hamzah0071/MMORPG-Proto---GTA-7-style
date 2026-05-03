import pygame
import pytmx
import pyscroll
import sys
from player import Player

from enemis import Enemy
from pnj import NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("GTA Slime ")
        
        self.font = pygame.font.SysFont("Arial", 24, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        self.player_name = ""
        self.player_sprite = "player/player1.png"
        self.game_state = "MENU" # MENU, PLAYING, GAMEOVER

        # Chargement carte Tiled
        try:
            self.tmx_data = pytmx.util_pygame.load_pygame("asset/mapes/mape.tmx")
        except Exception as e:
            print(f"Erreur chargement TMX: {e}")
            # Fallback ou gestion d'erreur si nécessaire
            
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def show_menu(self):
        input_active = True
        selected_char = 0 # 0: Player1, 1: Fille
        
        while input_active:
            self.screen.fill((30, 30, 30))
            
            # Titre
            title = self.large_font.render("GTA SLIME", True, (255, 255, 0))
            self.screen.blit(title, (400 - title.get_width()//2, 50))
            
            # Saisie du nom
            name_label = self.font.render(f"Entrez votre nom: {self.player_name}_", True, (255, 255, 255))
            self.screen.blit(name_label, (100, 200))
            
            # Choix personnage
            char_label = self.font.render("Choisissez votre personnage (Flèches Gauche/Droite):", True, (255, 255, 255))
            self.screen.blit(char_label, (100, 300))
            
            # Affichage des options de perso
            color1 = (0, 255, 0) if selected_char == 0 else (100, 100, 100)
            color2 = (0, 255, 0) if selected_char == 1 else (100, 100, 100)
            
            p1_text = self.font.render("1. Player 1", True, color1)
            p2_text = self.font.render("2. player 2", True, color2)
            
            self.screen.blit(p1_text, (150, 350))
            self.screen.blit(p2_text, (450, 350))
            
            instruction = self.font.render("Appuyez sur ENTREE pour commencer", True, (200, 200, 200))
            self.screen.blit(instruction, (400 - instruction.get_width()//2, 500))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.player_name != "":
                        self.player_sprite = "player/player1.png" if selected_char == 0 else "player/player2.png"
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_LEFT:
                        selected_char = 0
                    elif event.key == pygame.K_RIGHT:
                        selected_char = 1
                    else:
                        if len(self.player_name) < 15 and event.unicode.isprintable():
                            self.player_name += event.unicode

    def setup_game(self):
        try:
            player_obj = self.tmx_data.get_object_by_name("player")
            px, py = player_obj.x, player_obj.y
        except:
            px, py = 100, 100 # Position par défaut si l'objet player n'est pas trouvé
            
        self.player = Player(px, py, self.player_sprite, self.player_name)

        self.enemies = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()

        # Parcourir tous les objets pour trouver ennemis et PNJ
        found_enemy = False
        found_npc = False
        
        for obj in self.tmx_data.objects:
            # Détection par nom ou par type (plus robuste)
            name = str(obj.name).lower() if obj.name else ""
            obj_type = str(obj.type).lower() if hasattr(obj, 'type') and obj.type else ""
            
            if "enemis" in name or "enemy" in obj_type:
                enemy = Enemy(obj.x, obj.y, sprite_path="player/player1.png")
                self.enemies.add(enemy)
                found_enemy = True
            elif "pnj" in name or "pnj" in name or "npc" in obj_type:
                # Essayer d'extraire le dialogue du nom (format: npc_Nom_Dialogue)
                parts = name.split("_", 2)
                npc_name = parts[1].capitalize() if len(parts) > 1 else "PNJ"
                dialogue = parts[2] if len(parts) > 2 else "Bonjour! Je suis un PNJ."
                
                npc = NPC(obj.x, obj.y, name=npc_name, sprite_path="player/player1.png", dialogue=dialogue)
                self.npcs.add(npc)
                found_npc = True

        # SI RIEN N'EST TROUVÉ DANS LE TMX : Ajouter des instances de secours pour que l'utilisateur voie le résultat
        if not found_enemy:
            print("Aucun objet 'enemy' trouvé dans le TMX, ajout d'ennemis de secours.")
            for i in range(3):
                self.enemies.add(Enemy(px + 150 + (i*80), py + 50, sprite_path="player/player1.png"))
        
        if not found_npc:
            print("Aucun objet 'npc' trouvé dans le TMX, ajout d'un PNJ de secours.")
            self.npcs.add(NPC(px + 100, py + 150, name="Guide", sprite_path="player/player1.png", dialogue="Je suis ici car aucun PNJ n'a été trouvé sur la carte!"))

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.player)
        for enemy in self.enemies:
            self.group.add(enemy)
        for npc in self.npcs:
            self.group.add(npc)
        
        self.current_dialogue = None
        self.dialogue_timer = 0
        self.dialogue_duration = 3000

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
        if self.player.health <= 0:
            self.game_state = "GAMEOVER"
            return

        self.player.update()
        for enemy in self.enemies:
            enemy.update(self.player)
        for npc in self.npcs:
            npc.update(self.player)
        
        self.group.update()

        for sprite in self.group.sprites():
            if hasattr(sprite, 'feet'):
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back()

        if self.player.is_attacking:
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

        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.health -= 0.5
                if self.player.health < 0: self.player.health = 0
        
        now = pygame.time.get_ticks()
        if now - self.dialogue_timer > self.dialogue_duration:
            self.current_dialogue = None
        
        for npc in self.npcs:
            if npc.is_player_nearby(self.player):
                npc.is_interacting = True
            else:
                npc.is_interacting = False

    def draw_ui(self):
        bar_width = 200
        bar_height = 20
        x, y = 20, 20
        pygame.draw.rect(self.screen, (100, 0, 0), (x, y, bar_width, bar_height))
        health_width = (self.player.health / self.player.max_health) * bar_width
        pygame.draw.rect(self.screen, (0, 200, 0), (x, y, health_width, bar_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        name_text = self.font.render(f"{self.player.name} - PV: {int(self.player.health)}", True, (255, 255, 255))
        self.screen.blit(name_text, (x, y + 25))
        
        if self.current_dialogue:
            npc_name, dialogue_text = self.current_dialogue
            dialogue_label = self.small_font.render(f"{npc_name}: {dialogue_text}", True, (255, 255, 100))
            dialogue_bg = pygame.Surface((dialogue_label.get_width() + 20, dialogue_label.get_height() + 10))
            dialogue_bg.fill((50, 50, 50))
            self.screen.blit(dialogue_bg, (20, 100))
            self.screen.blit(dialogue_label, (30, 105))
        
        nearby_npcs = [npc for npc in self.npcs if npc.is_player_nearby(self.player)]
        if nearby_npcs:
            info_text = self.small_font.render("Appuyez sur E pour interagir", True, (200, 200, 200))
            self.screen.blit(info_text, (20, 550))

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        subtext = self.font.render("Appuyez sur ENTREE pour recommencer", True, (255, 255, 255))
        self.screen.blit(text, (400 - text.get_width()//2, 250))
        self.screen.blit(subtext, (400 - subtext.get_width()//2, 350))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game_state = "MENU"
                    self.player_name = ""

    def run(self):
        clock = pygame.time.Clock()
        while True:
            if self.game_state == "MENU":
                self.show_menu()
                self.setup_game()
                self.game_state = "PLAYING"
            elif self.game_state == "PLAYING":
                self.player.save_location()
                for enemy in self.enemies: enemy.save_location()
                for npc in self.npcs: npc.save_location()
                self.handle_input()
                self.update()
                self.group.center(self.player.rect.center)
                self.group.draw(self.screen)
                self.draw_ui()
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.attack()
                        elif event.key == pygame.K_e:
                            for npc in self.npcs:
                                if npc.is_player_nearby(self.player):
                                    self.current_dialogue = (npc.name, npc.get_dialogue())
                                    self.dialogue_timer = pygame.time.get_ticks()
                                    break
                clock.tick(60)
            elif self.game_state == "GAMEOVER":
                self.show_game_over()
        pygame.quit()
