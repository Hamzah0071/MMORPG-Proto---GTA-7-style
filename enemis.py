import pygame
import math

class Enemy(pygame.sprite.Sprite):
    """Classe pour les ennemis avec IA de détection et poursuite."""
    
    def __init__(self, x, y, sprite_path="player/player1.png", sprite_size=32):
        super().__init__()
        
        # Chargement du sprite
        try:
            self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            self.sprite_size = sprite_size
            self.image = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # On prend la première frame (face vers le bas)
            self.image.blit(self.sprite_sheet, (0, 0), (0, 0, sprite_size, sprite_size))
        except:
            self.image = pygame.Surface((sprite_size, sprite_size))
            self.image.fill((255, 0, 0))  # Rouge si image non trouvée
            self.sprite_size = sprite_size
        
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.rect.topleft = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        
        # Stats de l'ennemi
        self.speed = 0.5

        self.health = 30
        self.max_health = 30
        
        # IA - Détection et poursuite
        self.detection_radius = 9 * 32  # 9px en pixels (9 * 32 pour la grille)
        self.spawn_x = x  # Position d'origine
        self.spawn_y = y
        self.max_distance_from_spawn = 50 * 32  # 50px en pixels
        self.is_pursuing = False
        self.pursue_timer = 0
        
        # Mouvement aléatoire
        self.move_timer = 0
        self.direction = 'idle'
        self.random_move_interval = 1500  # ms
    
    def save_location(self):
        """Sauvegarde la position actuelle."""
        self.old_position = self.position.copy()
    
    def move_back(self):
        """Revient à la position précédente (collision)."""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def distance_to_player(self, player):
        """Calcule la distance entre l'ennemi et le joueur."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return math.sqrt(dx**2 + dy**2)
    
    def distance_from_spawn(self):
        """Calcule la distance entre l'ennemi et son point de spawn."""
        dx = self.position[0] - self.spawn_x
        dy = self.position[1] - self.spawn_y
        return math.sqrt(dx**2 + dy**2)
    
    def pursue_player(self, player):
        """Poursuit le joueur si détecté."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normaliser la direction
            dx /= distance
            dy /= distance
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed
            
            # Mettre à jour la direction pour l'animation
            if abs(dx) > abs(dy):
                self.direction = 'right' if dx > 0 else 'left'
            else:
                self.direction = 'down' if dy > 0 else 'up'
    
    def random_walk(self):
        """Mouvement aléatoire quand l'ennemi n'est pas en poursuite."""
        now = pygame.time.get_ticks()
        
        if now - self.move_timer > self.random_move_interval:
            import random
            self.direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
            self.move_timer = now
        
        if self.direction == 'up':
            self.position[1] -= self.speed
        elif self.direction == 'down':
            self.position[1] += self.speed
        elif self.direction == 'left':
            self.position[0] -= self.speed
        elif self.direction == 'right':
            self.position[0] += self.speed
    
    def update(self, player=None):
        """Met à jour l'ennemi."""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        if player is None:
            # Si pas de joueur, mouvement aléatoire
            self.random_walk()
            return
        
        # Vérifier si le joueur est dans le rayon de détection
        distance_to_player = self.distance_to_player(player)
        distance_from_spawn = self.distance_from_spawn()
        
        # Si le joueur est détecté et l'ennemi n'est pas trop loin de son spawn
        if distance_to_player < self.detection_radius and distance_from_spawn < self.max_distance_from_spawn:
            self.is_pursuing = True
            self.pursue_timer = pygame.time.get_ticks()
            self.pursue_player(player)
        # Si l'ennemi était en poursuite mais le joueur s'éloigne trop du spawn
        elif distance_from_spawn >= self.max_distance_from_spawn:
            self.is_pursuing = False
            # Retourner vers le spawn
            dx = self.spawn_x - self.rect.centerx
            dy = self.spawn_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.position[0] += dx * self.speed
                self.position[1] += dy * self.speed
        else:
            # Mouvement aléatoire
            self.is_pursuing = False
            self.random_walk()
