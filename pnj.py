import pygame
import math

class NPC(pygame.sprite.Sprite):
    """Classe pour les PNJ (Personnages Non Joueurs) avec dialogues."""
    
    def __init__(self, x, y, name="PNJ", sprite_path="player/player1.png", sprite_size=32, dialogue="Bonjour!"):
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
            self.image.fill((0, 255, 0))  # Vert si image non trouvée
            self.sprite_size = sprite_size
        
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.rect.topleft = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        
        # Infos du PNJ
        self.name = name
        self.dialogue = dialogue  # Texte que le PNJ va dire
        self.interaction_radius = 5 * 32  # Rayon d'interaction (5px en pixels)
        self.is_interacting = False
        self.direction = 'down'
    
    def save_location(self):
        """Sauvegarde la position actuelle."""
        self.old_position = self.position.copy()
    
    def move_back(self):
        """Revient à la position précédente (collision)."""
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
    
    def distance_to_player(self, player):
        """Calcule la distance entre le PNJ et le joueur."""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        return math.sqrt(dx**2 + dy**2)
    
    def is_player_nearby(self, player):
        """Vérifie si le joueur est à proximité pour interagir."""
        return self.distance_to_player(player) < self.interaction_radius
    
    def get_dialogue(self):
        """Retourne le dialogue du PNJ."""
        return self.dialogue
    
    def set_dialogue(self, new_dialogue):
        """Change le dialogue du PNJ."""
        self.dialogue = new_dialogue
    
    def update(self, player=None):
        """Met à jour le PNJ."""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        # Les PNJ ne se déplacent pas pour l'instant (statiques)
        # Vous pouvez ajouter des animations ou des mouvements ici si nécessaire
