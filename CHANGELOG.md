# 📝 CHANGELOG - GTA-7 MMORPG

## Version 2.0.0 - 🎮 Île UNKNOW (Mise à jour majeure)

### ✨ Nouvelles Fonctionnalités

#### Système de Cartographie
- ✅ **Fog of War** : Brouillard noir couvrant les zones non découvertes
- ✅ **Découverte progressive** : Les tuiles se découvrent en se déplaçant
- ✅ **Pourcentage de cartographie** : Affichage du % découvert en temps réel
- ✅ **Rayon de découverte** : 5 tuiles autour du joueur

#### Système de Bombes
- ✅ **Ramassage** : Les bombes jaunes se ramassent automatiquement
- ✅ **Inventaire** : Affichage du nombre de bombes
- ✅ **Lancer** : Clic souris pour lancer vers une cible
- ✅ **Explosion** : Rayon d'explosion avec dégâts progressifs
- ✅ **Destruction** : Les bombes éliminent les monstres

#### Monstres Améliorés
- ✅ **Aspiration d'âme** : Attaque spéciale qui inflige des dégâts progressifs
- ✅ **IA améliorée** : Poursuite intelligente du joueur
- ✅ **Détection** : Rayon de détection de 9 tuiles
- ✅ **Cooldown** : Système de cooldown pour les attaques
- ✅ **Santé** : Affichage de la barre de santé des monstres

#### Interface Utilisateur
- ✅ **HUD amélioré** : Affichage des statistiques en temps réel
- ✅ **Boîtes de dialogue** : Dialogues enrichis avec wrapping
- ✅ **Barre de santé** : Affichage visuel de la santé
- ✅ **Instructions** : Affichage des contrôles à l'écran
- ✅ **Écran de fin** : Affichage du pourcentage de cartographie

#### Dialogues des PNJ
- ✅ **Sage** : Conseils sur la cartographie et les monstres
- ✅ **Voyageur** : Informations sur les monstres
- ✅ **Chercheur** : Encouragements pour l'exploration
- ✅ **Interaction** : Système E pour interagir

#### Nouvelle Carte
- ✅ **Île UNKNOW** : Carte 60x40 tuiles avec plusieurs biomes
- ✅ **Biomes** : Forêt, eau, rochers, sable, zones mystérieuses
- ✅ **Fallback** : Charge mape.tmx si unknow.tmx n'existe pas

### 🔧 Améliorations Techniques

#### Architecture
- ✅ **Configuration centralisée** : Fichier config.py pour tous les paramètres
- ✅ **Système d'événements** : EventManager pour les interactions
- ✅ **Utilitaires UI** : Composants réutilisables (HUD, DialogueBox, etc.)
- ✅ **Code modulaire** : Séparation claire des responsabilités

#### Performance
- ✅ **Optimisation du rendu** : Rendu du fog of war optimisé
- ✅ **Gestion des sprites** : Utilisation efficace des groupes Pygame
- ✅ **Mise à jour d'IA** : Cooldown pour les calculs d'IA

#### Qualité du Code
- ✅ **Documentation** : Commentaires et docstrings complets
- ✅ **Gestion d'erreurs** : Fallback pour les assets manquants
- ✅ **Tests** : Script de test complet (test_game.py)

### 📚 Documentation

- ✅ **README_UNKNOW.md** : Guide du jeu avec histoire et objectifs
- ✅ **GUIDE_COMPLET.md** : Guide détaillé avec stratégies et dépannage
- ✅ **CHANGELOG.md** : Ce fichier

### 🎮 Équilibrage du Jeu

| Élément | Valeur | Notes |
|---------|--------|-------|
| Santé joueur | 100 | Pas de soin pour l'instant |
| Dégâts épée | 1 | Très lent, non recommandé |
| Dégâts bombe | 25 | Arme principale |
| Santé monstre | 30 | Facile à éliminer |
| Dégâts monstre | 2/frame | Dangereux en groupe |
| Rayon détection | 9 tuiles | Bon équilibre |
| Rayon explosion | 80 pixels | Couvre plusieurs tuiles |

### 🐛 Corrections de Bugs

- ✅ Collision des murs : Système de collision amélioré
- ✅ Dialogues : Affichage correct des dialogues
- ✅ Inventaire : Gestion correcte des bombes
- ✅ Fog of war : Rendu correct du brouillard

### ⚙️ Fichiers Modifiés

| Fichier | Type | Description |
|---------|------|-------------|
| game.py | Modifié | Intégration fog of war, bombes, carte UNKNOW |
| enemis.py | Modifié | Ajout aspiration d'âme, IA améliorée |
| pnj.py | Modifié | Dialogues enrichis, système de dialogue |
| player.py | Inchangé | Fonctionnalités existantes conservées |
| main.py | Inchangé | Point d'entrée inchangé |

### 📦 Nouveaux Fichiers

| Fichier | Description |
|---------|-------------|
| bomb.py | Système de bombes |
| fog_of_war.py | Système de cartographie |
| config.py | Configuration centralisée |
| events.py | Système d'événements |
| ui_utils.py | Utilitaires d'interface |
| test_game.py | Script de test |
| README_UNKNOW.md | Guide du jeu |
| GUIDE_COMPLET.md | Guide détaillé |
| CHANGELOG.md | Ce fichier |

### 🎯 Objectifs Atteints

- ✅ Cartographie progressive avec fog of war
- ✅ Monstres qui aspirent l'âme du joueur
- ✅ Système de bombes comme armes
- ✅ Île UNKNOW chargée et explorable
- ✅ Dialogues enrichis des PNJ
- ✅ Interface HUD améliorée
- ✅ Documentation complète

---

## Version 1.0.0 - Base du Jeu

### Fonctionnalités Initiales
- Système de joueur avec animations
- Système d'ennemis avec IA
- Système de PNJ avec dialogues
- Carte Tiled chargée
- Système de combat basique
- Interface HUD basique

---

## Prochaines Améliorations (v3.0.0)

- [ ] Système de soin (potions)
- [ ] Nouveaux types d'ennemis
- [ ] Boss final
- [ ] Quêtes et objectifs
- [ ] Sauvegarde de progression
- [ ] Musique et effets sonores
- [ ] Niveaux de difficulté
- [ ] Multiplayer local
- [ ] Nouveaux biomes
- [ ] Système de compétences

---

## Notes de Développement

### Décisions de Design

1. **Fog of War** : Choix d'un brouillard noir semi-transparent pour la clarté
2. **Bombes** : Arme principale pour éviter les combats directs trop difficiles
3. **Aspiration d'âme** : Attaque spéciale des monstres pour plus de tension
4. **Cartographie** : Objectif principal pour donner un sens à l'exploration

### Défis Rencontrés

1. **Performance** : Optimisation du rendu du fog of war
2. **Collision** : Gestion correcte des collisions avec les murs
3. **IA** : Équilibrage de la difficulté des monstres

### Solutions Apportées

1. **Performance** : Rendu optimisé avec zones visibles uniquement
2. **Collision** : Système de collision amélioré avec fallback
3. **IA** : Cooldown et rayon de détection ajustables

---

## Statistiques

- **Lignes de code** : ~2500+
- **Fichiers** : 13
- **Fonctionnalités** : 20+
- **Temps de développement** : Estimé 10-15 heures

---

**Dernière mise à jour** : Mai 2026

Pour toute question ou suggestion, consultez le fichier README_UNKNOW.md ou GUIDE_COMPLET.md.
