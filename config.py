"""
Configuration du jeu GTA-7 MMORPG
"""

# Écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Joueur
PLAYER_SPEED = 3
PLAYER_MAX_HEALTH = 100
PLAYER_ATTACK_COOLDOWN = 600  # ms

# Ennemis
ENEMY_SPEED = 0.8
ENEMY_HEALTH = 30
ENEMY_DETECTION_RADIUS = 9 * 32  # 9 tuiles
ENEMY_MAX_DISTANCE_FROM_SPAWN = 50 * 32  # 50 tuiles
ENEMY_SOUL_DRAIN_RANGE = 32  # pixels
ENEMY_SOUL_DRAIN_DAMAGE = 2  # par frame
ENEMY_SOUL_DRAIN_COOLDOWN = 500  # ms

# Bombes
BOMB_SPEED = 5  # pixels par frame
BOMB_EXPLOSION_RADIUS = 80  # pixels
BOMB_EXPLOSION_DAMAGE = 25  # dégâts
BOMB_EXPLOSION_DURATION = 500  # ms

# Fog of War
FOG_DISCOVERY_RADIUS = 5  # tuiles
FOG_COLOR = (20, 20, 40)
FOG_ALPHA = 200

# Cartes
MAP_TILE_SIZE = 32
MAP_ZOOM = 2

# Dialogues
DIALOGUE_DURATION = 3000  # ms

# Chemins des assets
ASSET_PATH = "asset/"
PLAYER_SPRITE_PATH = "player/player1.png"
ENEMY_SPRITE_PATH = "player/boss.png"
NPC_SPRITE_PATH = "player/Player.png"
BOMB_SPRITE_PATH = "asset/bombe.png"

# Cartes
MAP_UNKNOW = "asset/mapes/mape.tmx"
MAP_DEFAULT = "asset/mapes/mape.tmx"

# Dialogues des PNJ
NPC_DIALOGUES = {
    "Sage": [
        "Bienvenue sur UNKNOW!",
        "Cartographie cette île mystérieuse.",
        "Les monstres aspirent les âmes... Sois prudent!",
        "Trouve les bombes pour combattre les créatures."
    ],
    "Voyageur": [
        "J'ai vu des monstres au nord.",
        "Les bombes sont ta meilleure arme.",
        "Bonne chance dans ton exploration!"
    ],
    "Chercheur": [
        "Chaque tuile découverte nous aide.",
        "L'île UNKNOW cache de nombreux secrets.",
        "Continue ton exploration!"
    ]
}

# Couleurs
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_CYAN = (0, 255, 255)
COLOR_DARK_GRAY = (50, 50, 50)
COLOR_LIGHT_GRAY = (200, 200, 200)
COLOR_HEALTH_BAR_BG = (100, 0, 0)
COLOR_HEALTH_BAR_FG = (0, 200, 0)
COLOR_DIALOGUE_BG = (50, 50, 50)
COLOR_DIALOGUE_TEXT = (255, 255, 100)
COLOR_UI_TEXT = (255, 255, 255)

# Polices
FONT_LARGE = ("Arial", 50, True)
FONT_NORMAL = ("Arial", 24, True)
FONT_SMALL = ("Arial", 16, False)
