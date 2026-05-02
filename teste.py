import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.sprite_sheet = pygame.image.load("player/pixel_character_pale_blue_original.png").convert_alpha()
        self.frame_size = 32

        def get_frame(x, y):
            surf = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
            surf.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
            return surf

        self.animations = {
            'down': [get_frame(i * 32, 0) for i in range(4)],
            'left': [get_frame(i * 32, 32) for i in range(4)],
            'right': [get_frame(i * 32, 64) for i in range(4)],
            'up': [get_frame(i * 32, 96) for i in range(4)],
        }

        self.image = self.animations['down'][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = pygame.math.Vector2(x, y)

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.6, 12)
        self.feet.midbottom = self.rect.midbottom

        self.old_position = self.position.copy()

        self.direction = 'down'
        self.frame_index = 0
        self.animation_timer = 0

        self.walk_speed = 140  # ms/frame marche
        self.shoot_speed = 45  # ms/frame tir → très rapide pour effet "bang"

        self.moving = False
        self.speed = 3.0

        self.is_attacking = False
        self.attack_cooldown = 450
        self.last_attack = 0

        self.recoil = {'down': (0, 6), 'up': (0, -6), 'left': (-6, 0), 'right': (6, 0)}
        self.shake_amount = 0

    def save_location(self):
        self.old_position = self.position.copy()

    def move(self, dx, dy):
        if self.is_attacking:
            return
        if dx == 0 and dy == 0:
            self.moving = False
            return

        self.moving = True
        vec = pygame.math.Vector2(dx, dy)
        if vec.length() > 0:
            vec.normalize_ip()
            vec *= self.speed

        self.position += vec

        # Direction principale
        if abs(dx) > abs(dy):
            self.direction = 'right' if dx > 0 else 'left'
        else:
            self.direction = 'down' if dy > 0 else 'up'

    def attack(self):
        now = pygame.time.get_ticks()
        if self.is_attacking or now - self.last_attack < self.attack_cooldown:
            return

        self.is_attacking = True
        self.frame_index = 0
        self.animation_timer = now
        self.last_attack = now

        # Recul + shake initial
        rx, ry = self.recoil[self.direction]
        self.position.x += rx
        self.position.y += ry
        self.shake_amount = 3

    def update(self):
        now = pygame.time.get_ticks()
        shake_offset = 0

        if self.is_attacking:
            anim = self.animations[self.direction]
            speed = self.shoot_speed

            if now - self.animation_timer >= speed:
                self.animation_timer = now
                self.frame_index += 1
                if self.frame_index >= len(anim):
                    self.frame_index = 0
                    self.is_attacking = False
                    self.shake_amount = 0
                    # Option : annuler recul ici
                    # rx, ry = self.recoil[self.direction]
                    # self.position.x -= rx
                    # self.position.y -= ry

            # Shake pendant les 2 premières frames du tir
            if self.frame_index <= 1:
                shake_offset = self.shake_amount if now % 80 < 40 else -self.shake_amount
                self.shake_amount = max(0, self.shake_amount - 0.5)

        else:
            anim = self.animations[self.direction]
            speed = self.walk_speed

            if self.moving:
                if now - self.animation_timer >= speed:
                    self.animation_timer = now
                    self.frame_index = (self.frame_index + 1) % len(anim)
            else:
                self.frame_index = 0  # idle

        self.image = anim[self.frame_index]

        # Appliquer position + shake
        self.rect.topleft = (self.position.x + shake_offset, self.position.y)
        self.feet.midbottom = self.rect.midbottom

        self.moving = False  # reset, sera remis par move()

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

# Exemple d'utilisation rapide (test standalone)
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    player = Player(400, 300)
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        player.move(dx, dy)

        if keys[pygame.K_SPACE]:
            player.attack()

        player.update()

        screen.fill((20, 30, 20))
        all_sprites.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), player.feet, 1)  # debug pieds

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()