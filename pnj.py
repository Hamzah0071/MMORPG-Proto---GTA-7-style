import pygame
import math

class NPC(pygame.sprite.Sprite):
    """Classe pour les PNJ (Personnages Non Joueurs) avec dialogues enrichis."""
    
    def __init__(self, x, y, name="PNJ", sprite_path="player/paul.png", sprite_size=32, dialogue="Bonjour!"):
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
        self.interaction_radius = 5 * 32  # Rayon d'interaction (5 tuiles en pixels)
        self.is_interacting = False
        self.direction = 'down'
        
        # Dialogues multiples
        self.dialogue_list = [dialogue]  # Liste de dialogues possibles
        self.current_dialogue_index = 0
        
        # Animation d'interaction
        self.is_talking = False
        self.talk_timer = 0
        self.talk_duration = 3000  # ms
    
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
        """Retourne le dialogue actuel du PNJ."""
        return self.dialogue_list[self.current_dialogue_index % len(self.dialogue_list)]
    
    def next_dialogue(self):
        """Passe au dialogue suivant."""
        self.current_dialogue_index += 1
        return self.get_dialogue()
    
    def set_dialogue(self, new_dialogue):
        """Change le dialogue du PNJ."""
        if isinstance(new_dialogue, list):
            self.dialogue_list = new_dialogue
            self.current_dialogue_index = 0
        else:
            self.dialogue_list = [new_dialogue]
            self.current_dialogue_index = 0
        self.dialogue = self.dialogue_list[0]
    
    def set_talking(self, is_talking):
        """Marque le PNJ comme en train de parler."""
        self.is_talking = is_talking
        if is_talking:
            self.talk_timer = pygame.time.get_ticks()
    
    def is_talking_finished(self):
        """Vérifie si le PNJ a fini de parler."""
        if self.is_talking:
            elapsed = pygame.time.get_ticks() - self.talk_timer
            return elapsed > self.talk_duration
        return False
    
    def update(self, player=None):
        """Met à jour le PNJ."""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        
        # Vérifier si le dialogue est terminé
        if self.is_talking and self.is_talking_finished():
            self.is_talking = False
