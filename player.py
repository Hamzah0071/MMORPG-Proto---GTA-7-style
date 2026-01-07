import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player/player1.png").convert_alpha()
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed = 3

        # Animations adaptées Pipoya : 4 frames/dir, rows: down(0), left(32), right(64), up(96)
        self.animations = {
            'down':  [self.get_image(i * 32, 0) for i in range(4)],
            'left':  [self.get_image(i * 32, 32) for i in range(4)],
            'right': [self.get_image(i * 32, 64) for i in range(4)],
            'up':    [self.get_image(i * 32, 96) for i in range(4)],

            # Attacks réutilisent walk (proto) - plus tard vraie anim
            'attack_down':  [self.get_image(i * 32, 0) for i in range(4)],
            'attack_left':  [self.get_image(i * 32, 32) for i in range(4)],
            'attack_right': [self.get_image(i * 32, 64) for i in range(4)],
            'attack_up':    [self.get_image(i * 32, 96) for i in range(4)],
        }

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()

        self.direction = 'down'
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 150  # ms, adapté 4 frames
        self.moving = False

        # Attaque (réutilise walk, cooldown OK)
        self.is_attacking = False
        self.attack_cooldown = 600
        self.last_attack_time = 0

    def get_image(self, x, y):
        image = pygame.Surface((32, 32), pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
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
            self.animation_speed = 80  # Plus rapide en attaque !

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
                    self.animation_speed = 150  # Reset vitesse
                self.image = animation[self.frame_index]
        else:
            if self.moving:
                if now - self.animation_timer > self.animation_speed:
                    self.animation_timer = now
                    self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
                    self.image = self.animations[self.direction][self.frame_index]
            else:
                self.image = self.animations[self.direction][0]  # Idle
                self.frame_index = 0

        self.moving = False

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom