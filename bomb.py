import pygame
import math

class Bomb(pygame.sprite.Sprite):
    """Classe pour les bombes - armes contre les monstres."""
    
    def __init__(self, x, y, sprite_path="asset/bombe.png", sprite_size=32):
        super().__init__()
        
        # Chargement du sprite
        try:
            self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            self.sprite_size = sprite_size
            self.image = pygame.Surface((sprite_size, sprite_size), pygame.SRCALPHA)
            # On prend la première frame
            self.image.blit(self.sprite_sheet, (0, 0), (0, 0, sprite_size, sprite_size))
        except:
            self.image = pygame.Surface((sprite_size, sprite_size))
            self.image.fill((255, 255, 0))  # Jaune si image non trouvée
            self.sprite_size = sprite_size
        
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.rect.topleft = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        
        # État de la bombe
        self.is_active = True  # La bombe peut être ramassée
        self.is_thrown = False  # La bombe a été lancée
        self.target_x = None
        self.target_y = None
        self.speed = 5
        self.explosion_radius = 80  # pixels
        self.explosion_time = 0
        self.is_exploding = False
        self.explosion_duration = 500  # ms
    
    def save_location(self):
        """Sauvegarde la position actuelle."""
        self.old_position = self.position.copy()
    
    def move_back(self):
        """Revient à la position précédente (collision)."""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def throw(self, target_x, target_y):
        """Lance la bombe vers une cible."""
        self.is_thrown = True
        self.target_x = target_x
        self.target_y = target_y
    
    def update(self):
        """Met à jour la bombe."""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        if self.is_thrown and self.target_x is not None and self.target_y is not None:
            # Calculer la direction vers la cible
            dx = self.target_x - self.position[0]
            dy = self.target_y - self.position[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > self.speed:
                # Normaliser et déplacer
                dx /= distance
                dy /= distance
                self.position[0] += dx * self.speed
                self.position[1] += dy * self.speed
            else:
                # La bombe a atteint sa cible - explosion !
                self.is_exploding = True
                self.explosion_time = pygame.time.get_ticks()
                self.is_thrown = False
    
    def is_explosion_finished(self):
        """Vérifie si l'explosion est terminée."""
        if self.is_exploding:
            elapsed = pygame.time.get_ticks() - self.explosion_time
            return elapsed > self.explosion_duration
        return False
    
    def get_explosion_rect(self):
        """Retourne le rectangle d'explosion."""
        return pygame.Rect(
            self.rect.centerx - self.explosion_radius,
            self.rect.centery - self.explosion_radius,
            self.explosion_radius * 2,
            self.explosion_radius * 2
        )
