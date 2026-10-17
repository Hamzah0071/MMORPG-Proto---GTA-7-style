# GTA-7 MMORPG - Île UNKNOW

## 🎮 Vue d'ensemble

Bienvenue dans **GTA-7 MMORPG**, un jeu d'exploration et de survie où vous incarnez **Silver**, un aventurier solitaire arrivé sur l'île mystérieuse **UNKNOW**. Votre mission : cartographier l'île et survivre aux dangers qui vous attendent.

## 📖 Histoire

Le personnage **Silver** arrive sur l'île **UNKNOW**, une terre inconnue sans cartes ni guides. Seul face aux monstres qui aspirent les âmes, Silver doit :
- **Cartographier** l'île pour permettre à d'autres de la visiter
- **Survivre** aux attaques des monstres
- **Trouver des bombes** pour combattre les créatures
- **Interagir** avec les PNJ pour obtenir des informations

## 🎯 Objectifs du jeu

1. **Cartographie** : Découvrir 100% de l'île (le fog of war disparaît au fur et à mesure)
2. **Survie** : Maintenir votre santé au-dessus de 0
3. **Combat** : Éliminer les monstres qui aspirent votre âme
4. **Exploration** : Trouver des bombes et des ressources

## 🕹️ Contrôles

| Touche | Action |
|--------|--------|
| **Flèches** ou **ZQSD** | Se déplacer |
| **ESPACE** | Attaquer (épée) |
| **Clic souris** | Lancer une bombe |
| **E** | Interagir avec les PNJ |
| **ENTREE** | Valider au menu |

## 🎮 Mécanique de jeu

### Cartographie (Fog of War)
- Les zones non découvertes sont couvertes par un brouillard noir
- En vous déplaçant, vous découvrez progressivement l'île
- Le pourcentage de cartographie s'affiche en haut à gauche
- **Objectif** : Atteindre 100% de découverte

### Monstres - Aspiration d'Âme
- Les monstres rouges vous poursuivent quand vous êtes à proximité
- Ils aspirent votre âme pour vous infliger des dégâts
- **Attaque** : Appuyez sur ESPACE pour attaquer avec votre épée
- **Dégâts** : Chaque coup inflige 1 point de dégâts au monstre

### Bombes - Arme Principale
- Trouvez des bombes jaunes sur la carte
- Ramassez-les automatiquement en passant dessus
- Lancez-les avec un **clic souris** sur la cible
- Les bombes explosent et infligent 25 points de dégâts aux monstres proches
- **Rayon d'explosion** : ~80 pixels

### PNJ et Dialogues
- Les PNJ cyan vous donnent des informations
- Approchez-vous et appuyez sur **E** pour interagir
- Écoutez leurs conseils pour survivre

### Santé et Ressources
- Votre santé maximale est de 100 points
- Les monstres vous infligent des dégâts progressifs
- Aucun système de soin pour l'instant (à ajouter)
- **Inventaire** : Affiche le nombre de bombes disponibles

## 📊 Statistiques du jeu

| Élément | Valeur |
|---------|--------|
| Santé maximale | 100 |
| Dégâts épée | 1 |
| Dégâts bombe | 25 |
| Rayon d'explosion | 80 pixels |
| Rayon de détection ennemi | 288 pixels (9 tuiles) |
| Rayon d'interaction PNJ | 160 pixels (5 tuiles) |
| Vitesse du joueur | 3 pixels/frame |
| Vitesse de l'ennemi | 0.8 pixels/frame |

## 🗺️ Carte UNKNOW

- **Dimensions** : 60x40 tuiles (1920x1280 pixels)
- **Taille des tuiles** : 32x32 pixels
- **Biomes** : Forêt, eau, rochers, sable, zones mystérieuses
- **Zoom** : 2x (affichage à 64x64 pixels)

## 🎨 Visuels

- **Sprites** : Assets Hyptosis Tile Art Batch (RPG Nature Tileset)
- **Personnages** : Silver, ennemis (Boss), PNJ
- **Bombes** : Sprites dédiés avec animation
- **Fog of War** : Brouillard noir semi-transparent

## 🚀 Comment lancer le jeu

```bash
python main.py
```

### Dépendances requises
```bash
pip install pygame pytmx pyscroll
```

## 📝 Fichiers du projet

| Fichier | Description |
|---------|-------------|
| `main.py` | Point d'entrée du jeu |
| `game.py` | Moteur de jeu principal |
| `player.py` | Classe du joueur (Silver) |
| `enemis.py` | Classe des monstres |
| `pnj.py` | Classe des PNJ |
| `bomb.py` | Classe des bombes |
| `fog_of_war.py` | Système de cartographie |
| `asset/mapes/unknow.tmx` | Carte Tiled de l'île UNKNOW |

## 🎯 Conseils de survie

1. **Découvrez d'abord** : Explorez lentement pour éviter les monstres
2. **Trouvez les bombes** : Elles sont votre meilleure arme
3. **Écoutez les PNJ** : Ils donnent des indices utiles
4. **Gestion de la santé** : Évitez les combats directs quand possible
5. **Stratégie** : Utilisez les bombes pour éliminer plusieurs monstres à la fois

## 🔮 Améliorations futures

- [ ] Système de soin (potions)
- [ ] Nouveaux types d'ennemis
- [ ] Quêtes et objectifs
- [ ] Sauvegarde de progression
- [ ] Musique et effets sonores
- [ ] Niveaux de difficulté
- [ ] Multiplayer local

## 📧 Crédits

- **Développement** : GTA-7 MMORPG Team
- **Assets** : Hyptosis, OpenGameArt
- **Framework** : Pygame, Tiled, PyTMX, PyscrollGroup

---

**Bonne chance, Silver ! Cartographie l'île UNKNOW et survit aux monstres !** 🗺️👹💣
