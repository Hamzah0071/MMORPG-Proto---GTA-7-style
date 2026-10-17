"""
Système d'événements et de gestion des interactions
"""

import pygame

class EventManager:
    """Gestionnaire des événements du jeu."""
    
    def __init__(self):
        self.events = []
        self.listeners = {}
    
    def subscribe(self, event_type, callback):
        """S'abonner à un type d'événement."""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def unsubscribe(self, event_type, callback):
        """Se désabonner d'un type d'événement."""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
    
    def emit(self, event_type, data=None):
        """Émettre un événement."""
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)
    
    def clear(self):
        """Effacer tous les événements."""
        self.events = []


class GameEvents:
    """Types d'événements du jeu."""
    
    # Événements du joueur
    PLAYER_MOVED = "player_moved"
    PLAYER_ATTACKED = "player_attacked"
    PLAYER_DAMAGED = "player_damaged"
    PLAYER_DIED = "player_died"
    PLAYER_HEALED = "player_healed"
    
    # Événements des ennemis
    ENEMY_SPAWNED = "enemy_spawned"
    ENEMY_DAMAGED = "enemy_damaged"
    ENEMY_DIED = "enemy_died"
    ENEMY_ATTACKED = "enemy_attacked"
    
    # Événements des bombes
    BOMB_PICKED_UP = "bomb_picked_up"
    BOMB_THROWN = "bomb_thrown"
    BOMB_EXPLODED = "bomb_exploded"
    
    # Événements des PNJ
    NPC_DIALOGUE_STARTED = "npc_dialogue_started"
    NPC_DIALOGUE_ENDED = "npc_dialogue_ended"
    
    # Événements de cartographie
    TILE_DISCOVERED = "tile_discovered"
    DISCOVERY_PERCENTAGE_CHANGED = "discovery_percentage_changed"
    
    # Événements de jeu
    GAME_STARTED = "game_started"
    GAME_PAUSED = "game_paused"
    GAME_RESUMED = "game_resumed"
    GAME_OVER = "game_over"


class InteractionSystem:
    """Système de gestion des interactions."""
    
    def __init__(self):
        self.active_interactions = []
    
    def add_interaction(self, interaction):
        """Ajouter une interaction."""
        self.active_interactions.append(interaction)
    
    def remove_interaction(self, interaction):
        """Retirer une interaction."""
        if interaction in self.active_interactions:
            self.active_interactions.remove(interaction)
    
    def update(self, delta_time):
        """Mettre à jour les interactions."""
        for interaction in self.active_interactions[:]:
            if interaction.is_finished():
                self.remove_interaction(interaction)
            else:
                interaction.update(delta_time)
    
    def get_active_interactions(self):
        """Obtenir les interactions actives."""
        return self.active_interactions


class Interaction:
    """Classe de base pour les interactions."""
    
    def __init__(self, duration=0):
        self.duration = duration
        self.elapsed_time = 0
        self.is_active = True
    
    def update(self, delta_time):
        """Mettre à jour l'interaction."""
        self.elapsed_time += delta_time
    
    def is_finished(self):
        """Vérifier si l'interaction est terminée."""
        if self.duration > 0:
            return self.elapsed_time >= self.duration
        return False
    
    def execute(self):
        """Exécuter l'interaction."""
        pass


class DialogueInteraction(Interaction):
    """Interaction de dialogue."""
    
    def __init__(self, npc_name, dialogue_text, duration=3000):
        super().__init__(duration)
        self.npc_name = npc_name
        self.dialogue_text = dialogue_text
    
    def execute(self):
        """Exécuter le dialogue."""
        print(f"{self.npc_name}: {self.dialogue_text}")


class CombatInteraction(Interaction):
    """Interaction de combat."""
    
    def __init__(self, attacker, target, damage):
        super().__init__()
        self.attacker = attacker
        self.target = target
        self.damage = damage
    
    def execute(self):
        """Exécuter l'attaque."""
        if hasattr(self.target, 'health'):
            self.target.health -= self.damage


class ItemPickupInteraction(Interaction):
    """Interaction de ramassage d'objet."""
    
    def __init__(self, item, player):
        super().__init__()
        self.item = item
        self.player = player
    
    def execute(self):
        """Exécuter le ramassage."""
        if hasattr(self.player, 'inventory'):
            self.player.inventory.append(self.item)


# Instance globale du gestionnaire d'événements
event_manager = EventManager()
interaction_system = InteractionSystem()
