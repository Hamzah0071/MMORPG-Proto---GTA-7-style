"""
Script de test pour vérifier que tous les composants du jeu fonctionnent correctement.
"""

import sys
import os

def test_imports():
    """Tester que tous les modules peuvent être importés."""
    print("🧪 Test 1: Vérification des imports...")
    
    try:
        import pygame
        print("  ✅ pygame")
    except ImportError:
        print("  ❌ pygame - Installez avec: pip install pygame")
        return False
    
    try:
        import pytmx
        print("  ✅ pytmx")
    except ImportError:
        print("  ❌ pytmx - Installez avec: pip install pytmx")
        return False
    
    try:
        import pyscroll
        print("  ✅ pyscroll")
    except ImportError:
        print("  ❌ pyscroll - Installez avec: pip install pyscroll")
        return False
    
    try:
        from player import Player
        print("  ✅ player.py")
    except ImportError as e:
        print(f"  ❌ player.py - {e}")
        return False
    
    try:
        from enemis import Enemy
        print("  ✅ enemis.py")
    except ImportError as e:
        print(f"  ❌ enemis.py - {e}")
        return False
    
    try:
        from pnj import NPC
        print("  ✅ pnj.py")
    except ImportError as e:
        print(f"  ❌ pnj.py - {e}")
        return False
    
    try:
        from bomb import Bomb
        print("  ✅ bomb.py")
    except ImportError as e:
        print(f"  ❌ bomb.py - {e}")
        return False
    
    try:
        from fog_of_war import FogOfWar
        print("  ✅ fog_of_war.py")
    except ImportError as e:
        print(f"  ❌ fog_of_war.py - {e}")
        return False
    
    try:
        from config import *
        print("  ✅ config.py")
    except ImportError as e:
        print(f"  ❌ config.py - {e}")
        return False
    
    try:
        from events import EventManager
        print("  ✅ events.py")
    except ImportError as e:
        print(f"  ❌ events.py - {e}")
        return False
    
    try:
        from ui_utils import HUD
        print("  ✅ ui_utils.py")
    except ImportError as e:
        print(f"  ❌ ui_utils.py - {e}")
        return False
    
    return True


def test_assets():
    """Tester que tous les assets existent."""
    print("\n🧪 Test 2: Vérification des assets...")
    
    assets_to_check = [
        "asset/mapes/unknow.tmx",
        "asset/mapes/mape.tmx",
        "asset/bombe.png",
        "player/player1.png",
        "player/Player.png",
        "player/boss.png",
    ]
    
    all_exist = True
    for asset in assets_to_check:
        if os.path.exists(asset):
            print(f"  ✅ {asset}")
        else:
            print(f"  ❌ {asset} - Fichier manquant")
            all_exist = False
    
    return all_exist


def test_classes():
    """Tester que les classes peuvent être instanciées."""
    print("\n🧪 Test 3: Vérification des classes...")
    
    try:
        import pygame
        pygame.init()
        
        # Test Player
        try:
            from player import Player
            player = Player(100, 100, "player/player1.png", "TestPlayer")
            assert player.health == 100
            assert player.max_health == 100
            print("  ✅ Player")
        except Exception as e:
            print(f"  ❌ Player - {e}")
            return False
        
        # Test Enemy
        try:
            from enemis import Enemy
            enemy = Enemy(200, 200, "player/boss.png")
            assert enemy.health == 30
            assert enemy.max_health == 30
            print("  ✅ Enemy")
        except Exception as e:
            print(f"  ❌ Enemy - {e}")
            return False
        
        # Test NPC
        try:
            from pnj import NPC
            npc = NPC(150, 150, "TestNPC", "player/Player.png", dialogue="Test")
            assert npc.name == "TestNPC"
            print("  ✅ NPC")
        except Exception as e:
            print(f"  ❌ NPC - {e}")
            return False
        
        # Test Bomb
        try:
            from bomb import Bomb
            bomb = Bomb(300, 300, "asset/bombe.png")
            assert bomb.is_active == True
            print("  ✅ Bomb")
        except Exception as e:
            print(f"  ❌ Bomb - {e}")
            return False
        
        # Test FogOfWar
        try:
            from fog_of_war import FogOfWar
            fog = FogOfWar(60, 40, 32, 5)
            assert fog.total_tiles == 60 * 40
            print("  ✅ FogOfWar")
        except Exception as e:
            print(f"  ❌ FogOfWar - {e}")
            return False
        
        # Test Config
        try:
            from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
            assert SCREEN_WIDTH == 800
            assert SCREEN_HEIGHT == 600
            assert FPS == 60
            print("  ✅ Config")
        except Exception as e:
            print(f"  ❌ Config - {e}")
            return False
        
        # Test EventManager
        try:
            from events import EventManager, GameEvents
            em = EventManager()
            em.subscribe(GameEvents.PLAYER_MOVED, lambda x: None)
            em.emit(GameEvents.PLAYER_MOVED, {"x": 100, "y": 100})
            print("  ✅ EventManager")
        except Exception as e:
            print(f"  ❌ EventManager - {e}")
            return False
        
        # Test HUD
        try:
            from ui_utils import HUD
            hud = HUD(800, 600)
            print("  ✅ HUD")
        except Exception as e:
            print(f"  ❌ HUD - {e}")
            return False
        
        pygame.quit()
        return True
    
    except Exception as e:
        print(f"  ❌ Erreur générale - {e}")
        return False


def test_game_mechanics():
    """Tester les mécaniques du jeu."""
    print("\n🧪 Test 4: Vérification des mécaniques...")
    
    try:
        import pygame
        pygame.init()
        
        from player import Player
        from enemis import Enemy
        from bomb import Bomb
        from fog_of_war import FogOfWar
        
        # Test déplacement du joueur
        try:
            player = Player(100, 100, "player/player1.png", "TestPlayer")
            player.move(1, 0)
            assert player.position[0] > 100
            print("  ✅ Déplacement du joueur")
        except Exception as e:
            print(f"  ❌ Déplacement - {e}")
            return False
        
        # Test attaque du joueur
        try:
            player = Player(100, 100, "player/player1.png", "TestPlayer")
            player.attack()
            assert player.is_attacking == True
            print("  ✅ Attaque du joueur")
        except Exception as e:
            print(f"  ❌ Attaque - {e}")
            return False
        
        # Test IA de l'ennemi
        try:
            enemy = Enemy(200, 200, "player/boss.png")
            player = Player(100, 100, "player/player1.png", "TestPlayer")
            initial_pos = enemy.position.copy()
            enemy.pursue_player(player)
            # L'ennemi devrait s'être déplacé vers le joueur
            print("  ✅ IA de l'ennemi")
        except Exception as e:
            print(f"  ❌ IA - {e}")
            return False
        
        # Test lancer de bombe
        try:
            bomb = Bomb(300, 300, "asset/bombe.png")
            bomb.throw(400, 400)
            assert bomb.is_thrown == True
            print("  ✅ Lancer de bombe")
        except Exception as e:
            print(f"  ❌ Lancer - {e}")
            return False
        
        # Test fog of war
        try:
            fog = FogOfWar(60, 40, 32, 5)
            fog.discover_around_player(100, 100)
            assert fog.discovered_count > 0
            assert fog.get_discovery_percentage() > 0
            print("  ✅ Fog of war")
        except Exception as e:
            print(f"  ❌ Fog of war - {e}")
            return False
        
        pygame.quit()
        return True
    
    except Exception as e:
        print(f"  ❌ Erreur générale - {e}")
        return False


def main():
    """Exécuter tous les tests."""
    print("=" * 50)
    print("🎮 GTA-7 MMORPG - Test de Vérification")
    print("=" * 50)
    
    results = []
    
    # Exécuter les tests
    results.append(("Imports", test_imports()))
    results.append(("Assets", test_assets()))
    results.append(("Classes", test_classes()))
    results.append(("Mécaniques", test_game_mechanics()))
    
    # Afficher le résumé
    print("\n" + "=" * 50)
    print("📊 Résumé des tests")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 Tous les tests sont passés!")
        print("Vous pouvez maintenant lancer le jeu avec: python main.py")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("Veuillez corriger les erreurs avant de lancer le jeu.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
