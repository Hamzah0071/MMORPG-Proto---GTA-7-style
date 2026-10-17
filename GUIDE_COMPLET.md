# 🎮 GTA-7 MMORPG - Guide Complet

## 📖 Table des matières

1. [Introduction](#introduction)
2. [Démarrage](#démarrage)
3. [Contrôles](#contrôles)
4. [Mécanique de jeu](#mécanique-de-jeu)
5. [Stratégies](#stratégies)
6. [Dépannage](#dépannage)

---

## Introduction

**GTA-7 MMORPG** est un jeu d'exploration et de survie où vous incarnez **Silver**, un aventurier courageux arrivé sur l'île mystérieuse **UNKNOW**.

### Histoire

Silver arrive sur une île inconnue sans cartes ni guides. Seul face aux dangers, il doit :
- Cartographier l'île pour permettre à d'autres de la visiter
- Survivre aux monstres qui aspirent les âmes
- Trouver des bombes pour combattre les créatures
- Interagir avec les habitants locaux (PNJ)

### Objectif Principal

Découvrir **100% de l'île** tout en restant vivant !

---

## Démarrage

### Installation

1. Assurez-vous que Python 3.7+ est installé
2. Installez les dépendances :
```bash
pip install pygame pytmx pyscroll
```

### Lancer le jeu

```bash
python main.py
```

### Menu principal

1. Entrez votre nom (max 15 caractères)
2. Choisissez votre personnage avec les flèches gauche/droite
3. Appuyez sur ENTREE pour commencer

---

## Contrôles

### Déplacement

| Touche | Action |
|--------|--------|
| **Flèches ↑↓←→** | Se déplacer dans les 4 directions |
| **Z** | Haut |
| **S** | Bas |
| **Q** | Gauche |
| **D** | Droite |

### Combat

| Touche | Action |
|--------|--------|
| **ESPACE** | Attaquer avec l'épée |
| **Clic souris** | Lancer une bombe |
| **Clic droit** | Viser (optionnel) |

### Interaction

| Touche | Action |
|--------|--------|
| **E** | Interagir avec les PNJ |
| **ENTREE** | Valider les dialogues |

### Système

| Touche | Action |
|--------|--------|
| **ESC** | Pause (à implémenter) |
| **M** | Carte (à implémenter) |

---

## Mécanique de jeu

### 1. Cartographie (Fog of War)

Le monde est couvert d'un brouillard noir. En vous déplaçant, vous découvrez progressivement l'île.

**Système de découverte :**
- Les tuiles à proximité de Silver deviennent visibles
- Rayon de découverte : 5 tuiles autour du joueur
- Pourcentage affiché en haut à gauche
- **Objectif** : Atteindre 100%

**Stratégie :**
- Explorez systématiquement chaque zone
- Suivez les chemins pour couvrir plus de terrain
- Évitez les monstres pour explorer tranquillement

### 2. Santé et Survie

Votre santé maximale est de **100 points**.

**Sources de dégâts :**
- Monstres qui aspirent votre âme : **2 points/frame**
- Pas d'autres sources de dégâts pour l'instant

**Gestion de la santé :**
- Évitez les combats directs quand possible
- Utilisez les bombes pour éliminer les monstres à distance
- Aucun système de soin pour l'instant (à implémenter)

**Fin du jeu :**
- Quand la santé atteint 0, c'est Game Over
- Vous verrez le pourcentage de cartographie atteint

### 3. Ennemis - Monstres

Les monstres rouges sont des créatures qui aspirent votre âme.

**Caractéristiques :**
- **Santé** : 30 points
- **Vitesse** : 0.8 pixels/frame (plus lent que vous)
- **Rayon de détection** : 288 pixels (9 tuiles)
- **Rayon d'attaque** : 32 pixels
- **Dégâts** : 2 points/frame quand à proximité

**Comportement :**
- Patrouille aléatoirement quand le joueur est loin
- Vous poursuit quand vous êtes détecté
- Essaie de vous atteindre pour aspirer votre âme
- Retourne à son point d'origine si vous vous éloignez trop

**Combat direct :**
- Appuyez sur ESPACE pour attaquer avec l'épée
- Chaque coup inflige **1 point de dégâts**
- Cooldown : 600ms entre les attaques
- **Non recommandé** : Trop lent, utilisez les bombes

### 4. Bombes - Arme Principale

Les bombes jaunes sont votre meilleure arme contre les monstres.

**Ramassage :**
- Passez simplement sur une bombe pour la ramasser
- Elle s'ajoute à votre inventaire
- Affichage du nombre de bombes en haut à gauche

**Lancer une bombe :**
1. Assurez-vous d'avoir au moins une bombe
2. Cliquez sur la zone cible avec la souris
3. La bombe se lance et vole vers la cible
4. Elle explose à l'arrivée

**Explosion :**
- **Rayon d'explosion** : 80 pixels
- **Dégâts** : 25 points au centre
- **Dégâts progressifs** : Moins de dégâts en s'éloignant du centre
- Affecte tous les monstres dans le rayon

**Stratégie :**
- Trouvez les bombes en explorant
- Utilisez-les pour éliminer les monstres à distance
- Visez les groupes de monstres pour maximiser les dégâts
- Économisez les bombes pour les combats difficiles

### 5. PNJ et Dialogues

Les PNJ cyan sont des habitants de l'île qui vous donnent des informations.

**Interaction :**
1. Approchez-vous d'un PNJ (rayon : 160 pixels)
2. Un message "Appuyez sur E pour interagir" s'affiche
3. Appuyez sur E pour lancer le dialogue
4. Le dialogue s'affiche dans une boîte en haut à gauche

**Dialogues disponibles :**

**Sage** (position initiale : 5, 5)
- "Bienvenue sur UNKNOW!"
- "Cartographie cette île mystérieuse."
- "Les monstres aspirent les âmes... Sois prudent!"
- "Trouve les bombes pour combattre les créatures."

**Voyageur** (position initiale : 10, 8)
- "J'ai vu des monstres au nord."
- "Les bombes sont ta meilleure arme."
- "Bonne chance dans ton exploration!"

**Chercheur** (position initiale : 15, 12)
- "Chaque tuile découverte nous aide."
- "L'île UNKNOW cache de nombreux secrets."
- "Continue ton exploration!"

**Conseils des PNJ :**
- Écoutez les conseils pour des stratégies
- Certains dialogues donnent des indices sur les ressources
- Les PNJ peuvent être consultés plusieurs fois

### 6. Interface HUD

**Barre de santé (haut gauche) :**
- Affiche votre santé actuelle / maximale
- Barre verte = santé restante
- Barre rouge = santé perdue

**Cartographie (haut gauche) :**
- Pourcentage de l'île découverte
- Objectif : 100%

**Inventaire (haut gauche) :**
- Nombre de bombes disponibles
- Utilisé pour le lancer de bombes

**Instructions (bas de l'écran) :**
- Rappel des contrôles principaux

---

## Stratégies

### Stratégie 1 : Exploration Prudente

**Objectif** : Cartographier sans mourir

1. Commencez par explorer les zones proches du spawn
2. Évitez les monstres en les contournant
3. Cherchez les bombes en priorité
4. Explorez systématiquement chaque zone

**Avantages :**
- Moins de risques
- Permet de trouver toutes les bombes
- Bonne pour apprendre le jeu

### Stratégie 2 : Combat Agressif

**Objectif** : Éliminer les monstres pour explorer librement

1. Trouvez les premières bombes
2. Utilisez-les pour éliminer les monstres
3. Explorez les zones dégagées
4. Cherchez plus de bombes

**Avantages :**
- Liberté de mouvement
- Plus rapide
- Satisfaisant

### Stratégie 3 : Équilibre

**Objectif** : Combiner exploration et combat

1. Explorez prudemment au début
2. Ramassez les bombes trouvées
3. Utilisez les bombes contre les monstres gênants
4. Continuez l'exploration

**Avantages :**
- Équilibré en difficulté
- Permet de progresser régulièrement
- Bonne gestion des ressources

### Conseils Généraux

1. **Santé** : Maintenez-la au-dessus de 50% si possible
2. **Bombes** : Cherchez-les activement, elles sont cruciales
3. **Monstres** : Évitez les combats directs, utilisez les bombes
4. **PNJ** : Écoutez leurs conseils pour des indices
5. **Cartographie** : Explorez méthodiquement pour couvrir 100%

---

## Dépannage

### Le jeu ne démarre pas

**Erreur** : `ModuleNotFoundError: No module named 'pygame'`

**Solution** :
```bash
pip install pygame pytmx pyscroll
```

### La carte ne charge pas

**Erreur** : `Erreur chargement UNKNOW`

**Solution** :
- Vérifiez que le fichier `asset/mapes/unknow.tmx` existe
- Vérifiez que les fichiers de tilesets existent dans `asset/mapes/`
- Le jeu utilise `mape.tmx` en fallback

### Les sprites ne s'affichent pas

**Problème** : Les personnages apparaissent en couleur unie

**Solution** :
- Vérifiez que les fichiers dans `player/` existent
- Vérifiez les chemins dans `game.py`
- Vérifiez que les fichiers PNG sont valides

### Le jeu est trop lent

**Problème** : FPS bas, lag

**Solution** :
- Réduisez le zoom dans `game.py` (actuellement 2x)
- Fermez les autres applications
- Vérifiez les ressources système

### Les bombes ne font rien

**Problème** : Les bombes n'explosent pas

**Solution** :
- Vérifiez que vous avez des bombes (inventaire)
- Cliquez à proximité, pas trop loin
- Attendez que la bombe atteigne la cible

### Les monstres ne se déplacent pas

**Problème** : Les monstres restent immobiles

**Solution** :
- Approchez-vous du monstre (rayon de détection : 288 pixels)
- Vérifiez que le monstre n'est pas bloqué par un mur
- Redémarrez le jeu

---

## FAQ

**Q : Comment augmenter ma santé ?**
A : Aucun système de soin pour l'instant. Évitez les monstres !

**Q : Où trouver les bombes ?**
A : Elles sont éparpillées sur la carte. Explorez pour les trouver.

**Q : Combien de monstres y a-t-il ?**
A : 3 monstres par défaut, mais vous pouvez en ajouter dans la carte Tiled.

**Q : Quel est le temps limite ?**
A : Aucun. Prenez votre temps pour explorer.

**Q : Puis-je sauvegarder ma progression ?**
A : Pas pour l'instant. À implémenter.

**Q : Y a-t-il d'autres niveaux ?**
A : Actuellement, une seule île (UNKNOW).

---

## Améliorations Futures

- [ ] Système de soin (potions)
- [ ] Nouveaux types d'ennemis
- [ ] Quêtes et objectifs
- [ ] Sauvegarde de progression
- [ ] Musique et effets sonores
- [ ] Niveaux de difficulté
- [ ] Multiplayer local
- [ ] Nouveaux biomes
- [ ] Boss final
- [ ] Système de compétences

---

**Bonne chance, Silver ! Cartographie l'île UNKNOW et survit aux monstres !** 🗺️👹💣

Pour toute question ou bug, consultez le fichier `README_UNKNOW.md`.
