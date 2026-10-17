"""
Utilitaires pour l'interface utilisateur
"""

import pygame
from config import *

class UIElement:
    """Classe de base pour les éléments d'interface."""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
    
    def draw(self, surface):
        """Dessiner l'élément."""
        pass
    
    def update(self, delta_time):
        """Mettre à jour l'élément."""
        pass
    
    def is_clicked(self, pos):
        """Vérifier si l'élément est cliqué."""
        return self.rect.collidepoint(pos)


class HealthBar(UIElement):
    """Barre de santé."""
    
    def __init__(self, x, y, width, height, entity):
        super().__init__(x, y, width, height)
        self.entity = entity
        self.bg_color = COLOR_HEALTH_BAR_BG
        self.fg_color = COLOR_HEALTH_BAR_FG
    
    def draw(self, surface):
        """Dessiner la barre de santé."""
        if not self.visible or not hasattr(self.entity, 'health'):
            return
        
        # Fond de la barre
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Barre de santé
        health_ratio = self.entity.health / self.entity.max_health
        health_width = self.rect.width * health_ratio
        health_rect = pygame.Rect(self.rect.x, self.rect.y, health_width, self.rect.height)
        pygame.draw.rect(surface, self.fg_color, health_rect)
        
        # Bordure
        pygame.draw.rect(surface, COLOR_WHITE, self.rect, 2)


class TextDisplay(UIElement):
    """Affichage de texte."""
    
    def __init__(self, x, y, text, font_name="Arial", font_size=24, bold=False, color=COLOR_WHITE):
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size, bold)
        self.color = color
        self.rendered_text = self.font.render(self.text, True, self.color)
        super().__init__(x, y, self.rendered_text.get_width(), self.rendered_text.get_height())
    
    def set_text(self, new_text):
        """Changer le texte."""
        self.text = new_text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.rect.width = self.rendered_text.get_width()
        self.rect.height = self.rendered_text.get_height()
    
    def draw(self, surface):
        """Dessiner le texte."""
        if self.visible:
            surface.blit(self.rendered_text, self.rect)


class DialogueBox(UIElement):
    """Boîte de dialogue."""
    
    def __init__(self, x, y, width, height, npc_name="", dialogue_text=""):
        super().__init__(x, y, width, height)
        self.npc_name = npc_name
        self.dialogue_text = dialogue_text
        self.bg_color = COLOR_DIALOGUE_BG
        self.text_color = COLOR_DIALOGUE_TEXT
        self.border_color = COLOR_WHITE
        self.padding = 10
        
        # Polices
        self.name_font = pygame.font.SysFont("Arial", 18, True)
        self.text_font = pygame.font.SysFont("Arial", 14, False)
    
    def set_dialogue(self, npc_name, dialogue_text):
        """Définir le dialogue."""
        self.npc_name = npc_name
        self.dialogue_text = dialogue_text
    
    def draw(self, surface):
        """Dessiner la boîte de dialogue."""
        if not self.visible:
            return
        
        # Fond
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # Bordure
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        
        # Nom du PNJ
        name_text = self.name_font.render(self.npc_name, True, self.text_color)
        surface.blit(name_text, (self.rect.x + self.padding, self.rect.y + self.padding))
        
        # Texte du dialogue (avec wrapping)
        y_offset = self.rect.y + self.padding + name_text.get_height() + 5
        max_width = self.rect.width - 2 * self.padding
        
        words = self.dialogue_text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            test_text = self.text_font.render(test_line, True, self.text_color)
            
            if test_text.get_width() > max_width:
                if current_line:
                    line_text = self.text_font.render(current_line, True, self.text_color)
                    surface.blit(line_text, (self.rect.x + self.padding, y_offset))
                    y_offset += line_text.get_height() + 2
                current_line = word + " "
            else:
                current_line = test_line
        
        # Dernière ligne
        if current_line:
            line_text = self.text_font.render(current_line, True, self.text_color)
            surface.blit(line_text, (self.rect.x + self.padding, y_offset))


class HUD:
    """Affichage HUD (Head-Up Display)."""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.elements = []
        self.font_small = pygame.font.SysFont("Arial", 16, False)
        self.font_normal = pygame.font.SysFont("Arial", 24, True)
    
    def add_element(self, element):
        """Ajouter un élément."""
        self.elements.append(element)
    
    def draw(self, surface):
        """Dessiner tous les éléments."""
        for element in self.elements:
            element.draw(surface)
    
    def update(self, delta_time):
        """Mettre à jour tous les éléments."""
        for element in self.elements:
            element.update(delta_time)
    
    def draw_player_stats(self, surface, player, fog_of_war, inventory):
        """Dessiner les statistiques du joueur."""
        x, y = 20, 20
        
        # Barre de santé
        bar_width = 200
        bar_height = 20
        pygame.draw.rect(surface, COLOR_HEALTH_BAR_BG, (x, y, bar_width, bar_height))
        health_width = (player.health / player.max_health) * bar_width
        pygame.draw.rect(surface, COLOR_HEALTH_BAR_FG, (x, y, health_width, bar_height))
        pygame.draw.rect(surface, COLOR_WHITE, (x, y, bar_width, bar_height), 2)
        
        # Texte de santé
        health_text = self.font_normal.render(f"{player.name} - PV: {int(player.health)}", True, COLOR_UI_TEXT)
        surface.blit(health_text, (x, y + 25))
        
        # Cartographie
        discovery_text = self.font_small.render(f"Cartographie: {fog_of_war.get_discovery_percentage()}%", True, (100, 200, 255))
        surface.blit(discovery_text, (x, y + 50))
        
        # Inventaire
        inventory_text = self.font_small.render(f"Bombes: {len(inventory)}", True, (255, 255, 100))
        surface.blit(inventory_text, (x, y + 70))
    
    def draw_instructions(self, surface):
        """Dessiner les instructions."""
        instructions = self.font_small.render("ESPACE: Attaquer | CLIC: Lancer Bombe | E: Interagir", True, (150, 150, 150))
        surface.blit(instructions, (self.screen_width // 2 - instructions.get_width() // 2, self.screen_height - 30))
    
    def draw_interaction_prompt(self, surface):
        """Dessiner le message d'interaction."""
        prompt_text = self.font_small.render("Appuyez sur E pour interagir", True, (200, 200, 200))
        surface.blit(prompt_text, (20, self.screen_height - 50))
    
    def draw_game_over(self, surface, discovery_percentage):
        """Dessiner l'écran de fin de jeu."""
        # Fond semi-transparent
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill(COLOR_BLACK)
        surface.blit(overlay, (0, 0))
        
        # Texte
        large_font = pygame.font.SysFont("Arial", 50, True)
        normal_font = pygame.font.SysFont("Arial", 24, True)
        
        game_over_text = large_font.render("GAME OVER", True, COLOR_RED)
        surface.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 200))
        
        discovery_text = normal_font.render(f"Vous avez cartographié {discovery_percentage}% de l'île", True, COLOR_WHITE)
        surface.blit(discovery_text, (self.screen_width // 2 - discovery_text.get_width() // 2, 300))
        
        restart_text = normal_font.render("Appuyez sur ENTREE pour recommencer", True, COLOR_WHITE)
        surface.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, 400))


class Tooltip:
    """Infobulle."""
    
    def __init__(self, text, x, y, duration=2000):
        self.text = text
        self.x = x
        self.y = y
        self.duration = duration
        self.creation_time = pygame.time.get_ticks()
        self.font = pygame.font.SysFont("Arial", 14, False)
        self.bg_color = COLOR_DARK_GRAY
        self.text_color = COLOR_WHITE
    
    def is_expired(self):
        """Vérifier si l'infobulle a expiré."""
        elapsed = pygame.time.get_ticks() - self.creation_time
        return elapsed > self.duration
    
    def draw(self, surface):
        """Dessiner l'infobulle."""
        text_surface = self.font.render(self.text, True, self.text_color)
        padding = 5
        bg_rect = pygame.Rect(self.x - padding, self.y - padding, 
                             text_surface.get_width() + 2 * padding, 
                             text_surface.get_height() + 2 * padding)
        
        pygame.draw.rect(surface, self.bg_color, bg_rect)
        pygame.draw.rect(surface, self.text_color, bg_rect, 1)
        surface.blit(text_surface, (self.x, self.y))
