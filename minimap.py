"""
Système de mini-carte (minimap) qui se révèle progressivement
Style Zelda/Adventure - petit carré noir qui se remplit au fur et à mesure
"""

import pygame
import math

class Minimap:
    """Mini-carte qui se révèle progressivement à mesure que le joueur explore."""
    
    def __init__(self, map_width, map_height, tile_size=32, minimap_size=150, position=(10, 10)):
        """
        Initialise la mini-carte.
        
        Args:
            map_width: Largeur de la carte en tuiles
            map_height: Hauteur de la carte en tuiles
            tile_size: Taille d'une tuile en pixels
            minimap_size: Taille de la mini-carte en pixels (carré)
            position: Position (x, y) de la mini-carte sur l'écran
        """
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.minimap_size = minimap_size
        self.position = position
        
        # Calcul de l'échelle (combien de pixels de la carte = 1 pixel de minimap)
        self.scale_x = (map_width * tile_size) / minimap_size
        self.scale_y = (map_height * tile_size) / minimap_size
        
        # Grille de tuiles découvertes
        self.discovered = [[False for _ in range(map_width)] for _ in range(map_height)]
        
        # Surface de la minimap
        self.surface = pygame.Surface((minimap_size, minimap_size))
        self.surface.fill((0, 0, 0))  # Noir au départ
        
        # Couleurs
        self.color_unknown = (0, 0, 0)  # Noir = inconnu
        self.color_discovered = (50, 100, 50)  # Vert foncé = découvert
        self.color_water = (30, 60, 100)  # Bleu = eau
        self.color_forest = (40, 80, 40)  # Vert = forêt
        self.color_player = (255, 255, 0)  # Jaune = joueur
        self.color_enemy = (255, 0, 0)  # Rouge = ennemi
        self.color_npc = (0, 255, 255)  # Cyan = PNJ
        self.color_border = (100, 100, 100)  # Gris = bordure
    
    def discover_tile(self, tile_x, tile_y):
        """Découvrir une tuile."""
        if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
            self.discovered[tile_y][tile_x] = True
    
    def discover_around_player(self, player_x, player_y, discovery_radius_tiles=5):
        """Découvrir les tuiles autour du joueur."""
        player_tile_x = player_x // self.tile_size
        player_tile_y = player_y // self.tile_size
        
        for dy in range(-discovery_radius_tiles, discovery_radius_tiles + 1):
            for dx in range(-discovery_radius_tiles, discovery_radius_tiles + 1):
                tile_x = player_tile_x + dx
                tile_y = player_tile_y + dy
                
                # Vérifier la distance (cercle)
                distance = math.sqrt(dx**2 + dy**2)
                if distance <= discovery_radius_tiles:
                    self.discover_tile(tile_x, tile_y)
    
    def update(self, tiles, player_x, player_y):
        """
        Mettre à jour la mini-carte.
        
        Args:
            tiles: Grille de tuiles de la carte
            player_x: Position X du joueur en pixels
            player_y: Position Y du joueur en pixels
        """
        # Effacer la surface
        self.surface.fill(self.color_unknown)
        
        # Dessiner les tuiles découvertes
        for tile_y in range(self.map_height):
            for tile_x in range(self.map_width):
                if self.discovered[tile_y][tile_x]:
                    # Calculer la position sur la minimap
                    mini_x = int((tile_x * self.tile_size) / self.scale_x)
                    mini_y = int((tile_y * self.tile_size) / self.scale_y)
                    mini_w = max(1, int(self.tile_size / self.scale_x))
                    mini_h = max(1, int(self.tile_size / self.scale_y))
                    
                    # Choisir la couleur selon le type de tuile
                    if tile_y < len(tiles) and tile_x < len(tiles[0]):
                        tile = tiles[tile_y][tile_x]
                        if hasattr(tile, 'type'):
                            if tile.type == 'water':
                                color = self.color_water
                            elif tile.type == 'forest':
                                color = self.color_forest
                            else:
                                color = self.color_discovered
                        else:
                            color = self.color_discovered
                    else:
                        color = self.color_discovered
                    
                    # Dessiner le pixel
                    pygame.draw.rect(self.surface, color, (mini_x, mini_y, mini_w, mini_h))
        
        # Dessiner le joueur
        player_mini_x = int((player_x / self.scale_x))
        player_mini_y = int((player_y / self.scale_y))
        pygame.draw.circle(self.surface, self.color_player, (player_mini_x, player_mini_y), 2)
        
        # Dessiner la bordure
        pygame.draw.rect(self.surface, self.color_border, (0, 0, self.minimap_size, self.minimap_size), 2)
    
    def draw(self, screen):
        """Dessiner la mini-carte sur l'écran."""
        screen.blit(self.surface, self.position)
    
    def draw_with_entities(self, screen, enemies=None, npcs=None):
        """
        Dessiner la mini-carte avec les ennemis et PNJ.
        
        Args:
            screen: Surface de l'écran
            enemies: Liste des ennemis
            npcs: Liste des PNJ
        """
        # D'abord dessiner la minimap
        self.draw(screen)
        
        # Dessiner les ennemis
        if enemies:
            for enemy in enemies:
                if self.discovered[int(enemy.position[1] // self.tile_size)][int(enemy.position[0] // self.tile_size)]:
                    enemy_mini_x = int((enemy.position[0] / self.scale_x)) + self.position[0]
                    enemy_mini_y = int((enemy.position[1] / self.scale_y)) + self.position[1]
                    pygame.draw.circle(screen, self.color_enemy, (enemy_mini_x, enemy_mini_y), 2)
        
        # Dessiner les PNJ
        if npcs:
            for npc in npcs:
                if self.discovered[int(npc.position[1] // self.tile_size)][int(npc.position[0] // self.tile_size)]:
                    npc_mini_x = int((npc.position[0] / self.scale_x)) + self.position[0]
                    npc_mini_y = int((npc.position[1] / self.scale_y)) + self.position[1]
                    pygame.draw.circle(screen, self.color_npc, (npc_mini_x, npc_mini_y), 2)
    
    def get_discovery_percentage(self):
        """Retourne le pourcentage de tuiles découvertes."""
        total_tiles = self.map_width * self.map_height
        discovered_count = sum(1 for row in self.discovered for tile in row if tile)
        return int((discovered_count / total_tiles) * 100) if total_tiles > 0 else 0
    
    def set_color(self, color_type, color):
        """Changer une couleur de la minimap."""
        if color_type == "unknown":
            self.color_unknown = color
        elif color_type == "discovered":
            self.color_discovered = color
        elif color_type == "water":
            self.color_water = color
        elif color_type == "forest":
            self.color_forest = color
        elif color_type == "player":
            self.color_player = color
        elif color_type == "enemy":
            self.color_enemy = color
        elif color_type == "npc":
            self.color_npc = color
        elif color_type == "border":
            self.color_border = color
