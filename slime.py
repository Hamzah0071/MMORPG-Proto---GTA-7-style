import pygame
import random

class Slime(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # On utilise une image existante ou une surface simple si l'image n'est pas dispo
        try:
            self.sprite_sheet = pygame.image.load("asset/BombExploding.png").convert_alpha()
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.blit(self.sprite_sheet, (0, 0), (0, 0, 32, 32))
        except:
            self.image = pygame.Surface((32, 32))
            self.image.fill((0, 255, 0)) # Vert pour un slime
            
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.rect.topleft = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.speed = 1
        
        self.health = 30
        self.move_timer = 0

    def save_location(self):
        self.old_position = self.position.copy()

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        # IA simple : bouge aléatoirement
        now = pygame.time.get_ticks()
        if now - self.move_timer > 1000:
            self.direction = random.choice(['up', 'down', 'left', 'right', 'idle'])
            self.move_timer = now
            
        if hasattr(self, 'direction'):
            if self.direction == 'up': self.position[1] -= self.speed
            elif self.direction == 'down': self.position[1] += self.speed
            elif self.direction == 'left': self.position[0] -= self.speed
            elif self.direction == 'right': self.position[0] += self.speed

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
