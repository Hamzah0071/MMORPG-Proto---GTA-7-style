import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path="player/player1.png", name="Joueur"):
        super().__init__()
        self.name = name
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        
        # On détecte la taille du sprite (32x32 par défaut)
        self.sprite_size = 32
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 3
        
        # PV du joueur
        self.max_health = 100
        self.health = 100
        
        # Animations (4 frames par direction)
        self.animations = {
            'down':  [self.get_image(i * self.sprite_size, 0) for i in range(4)],
            'left':  [self.get_image(i * self.sprite_size, self.sprite_size) for i in range(4)],
            'right': [self.get_image(i * self.sprite_size, self.sprite_size * 2) for i in range(4)],
            'up':    [self.get_image(i * self.sprite_size, self.sprite_size * 3) for i in range(4)],
            
            'attack_down':  [self.get_image(i * self.sprite_size, 0) for i in range(4)],
            'attack_left':  [self.get_image(i * self.sprite_size, self.sprite_size) for i in range(4)],
            'attack_right': [self.get_image(i * self.sprite_size, self.sprite_size * 2) for i in range(4)],
            'attack_up':    [self.get_image(i * self.sprite_size, self.sprite_size * 3) for i in range(4)],
        }

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        self.direction = 'down'
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.moving = False

        self.is_attacking = False
        self.attack_cooldown = 600
        self.last_attack_time = 0

    def get_image(self, x, y):
        image = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.sprite_size, self.sprite_size))
        return image

    def save_location(self):
        self.old_position = self.position.copy()

    def move(self, dx, dy):
        if not self.is_attacking:
            self.position[0] += dx * self.speed
            self.position[1] += dy * self.speed

    def attack(self):
        now = pygame.time.get_ticks()
        if not self.is_attacking and (now - self.last_attack_time > self.attack_cooldown):
            self.is_attacking = True
            self.frame_index = 0
            self.animation_timer = now
            self.last_attack_time = now
            self.animation_speed = 80

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        now = pygame.time.get_ticks()

        if self.is_attacking:
            anim_key = f"attack_{self.direction}"
            animation = self.animations[anim_key]
            if now - self.animation_timer > self.animation_speed:
                self.animation_timer = now
                self.frame_index += 1
                if self.frame_index >= len(animation):
                    self.frame_index = 0
                    self.is_attacking = False
                    self.animation_speed = 150
                self.image = animation[self.frame_index]
        else:
            if self.moving:
                if now - self.animation_timer > self.animation_speed:
                    self.animation_timer = now
                    self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
                    self.image = self.animations[self.direction][self.frame_index]
            else:
                self.image = self.animations[self.direction][0]
                self.frame_index = 0

        self.moving = False

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
