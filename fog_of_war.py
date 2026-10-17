import pygame
import math

class FogOfWar:
    """Système de brouillard de guerre pour la cartographie."""
    
    def __init__(self, map_width, map_height, tile_size=32, discovery_radius=5):
        """
        Initialise le fog of war.
        
        Args:
            map_width: Largeur de la carte en tuiles
            map_height: Hauteur de la carte en tuiles
            tile_size: Taille d'une tuile en pixels
            discovery_radius: Rayon de découverte autour du joueur (en tuiles)
        """
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.discovery_radius = discovery_radius
        
        # Grille de tuiles découvertes (True = découverte, False = non découverte)
        self.discovered = [[False for _ in range(map_width)] for _ in range(map_height)]
        
        # Surface pour le rendu du fog of war
        self.fog_surface = pygame.Surface((map_width * tile_size, map_height * tile_size))
        self.fog_surface.fill((0, 0, 0))
        self.fog_surface.set_alpha(200)  # Semi-transparent
        
        # Statistiques
        self.total_tiles = map_width * map_height
        self.discovered_count = 0
    
    def discover_around_player(self, player_x, player_y):
        """
        Découvre les tuiles autour du joueur.
        
        Args:
            player_x: Position X du joueur en pixels
            player_y: Position Y du joueur en pixels
        """
        # Convertir les pixels en tuiles
        player_tile_x = player_x // self.tile_size
        player_tile_y = player_y // self.tile_size
        
        # Découvrir les tuiles dans le rayon
        for dy in range(-self.discovery_radius, self.discovery_radius + 1):
            for dx in range(-self.discovery_radius, self.discovery_radius + 1):
                tile_x = player_tile_x + dx
                tile_y = player_tile_y + dy
                
                # Vérifier si la tuile est dans les limites
                if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
                    # Vérifier la distance (cercle, pas carré)
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance <= self.discovery_radius:
                        if not self.discovered[tile_y][tile_x]:
                            self.discovered[tile_y][tile_x] = True
                            self.discovered_count += 1
    
    def is_tile_discovered(self, tile_x, tile_y):
        """Vérifie si une tuile a été découverte."""
        if 0 <= tile_x < self.map_width and 0 <= tile_y < self.map_height:
            return self.discovered[tile_y][tile_x]
        return False
    
    def get_discovery_percentage(self):
        """Retourne le pourcentage de tuiles découvertes."""
        if self.total_tiles == 0:
            return 0
        return int((self.discovered_count / self.total_tiles) * 100)
    
    def update_fog_surface(self, camera_x, camera_y, screen_width, screen_height):
        """
        Met à jour la surface du fog of war pour le rendu.
        
        Args:
            camera_x: Position X de la caméra
            camera_y: Position Y de la caméra
            screen_width: Largeur de l'écran
            screen_height: Hauteur de l'écran
        """
        # Recréer la surface du fog
        self.fog_surface.fill((0, 0, 0))
        
        # Calculer les tuiles visibles
        start_tile_x = max(0, camera_x // self.tile_size)
        start_tile_y = max(0, camera_y // self.tile_size)
        end_tile_x = min(self.map_width, (camera_x + screen_width) // self.tile_size + 1)
        end_tile_y = min(self.map_height, (camera_y + screen_height) // self.tile_size + 1)
        
        # Dessiner le fog pour les tuiles non découvertes
        for tile_y in range(start_tile_y, end_tile_y):
            for tile_x in range(start_tile_x, end_tile_x):
                if not self.discovered[tile_y][tile_x]:
                    rect = pygame.Rect(
                        tile_x * self.tile_size,
                        tile_y * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    pygame.draw.rect(self.fog_surface, (0, 0, 0), rect)
    
    def draw(self, screen, camera_x, camera_y):
        """
        Dessine le fog of war sur l'écran.
        
        Args:
            screen: Surface de l'écran Pygame
            camera_x: Position X de la caméra
            camera_y: Position Y de la caméra
        """
        # Créer une surface temporaire pour le rendu
        temp_surface = pygame.Surface(screen.get_size())
        temp_surface.fill((0, 0, 0))
        
        # Dessiner le fog avec un masque circulaire autour du joueur
        for tile_y in range(self.map_height):
            for tile_x in range(self.map_width):
                if not self.discovered[tile_y][tile_x]:
                    rect = pygame.Rect(
                        tile_x * self.tile_size - camera_x,
                        tile_y * self.tile_size - camera_y,
                        self.tile_size,
                        self.tile_size
                    )
                    pygame.draw.rect(temp_surface, (20, 20, 40), rect)
        
        screen.blit(temp_surface, (0, 0))
