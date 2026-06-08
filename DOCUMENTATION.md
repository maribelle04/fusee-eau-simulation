# Fusée à eau - Simulation de vol

## Description

Ce projet a été réalisé dans le cadre du projet de classe des ESEO 2 de l'année scolaire 2025-2026. Il consiste en une **simulation numérique du vol d’une fusée à eau** (propulsion par éjection d’eau sous pression). Le code résout les équations de Bernoulli, de la détente adiabatique de l’air et du principe fondamental de la dynamique pour estimer la poussée, la vitesse, la hauteur et l’évolution du volume d’air au cours du temps.

## Auteurs

Projet réalisé par les élèves de l'ESEO 2  
Classe préparatoire – ESEO- Cours lumière 

## Fonctionnalités

- Calcul de la **poussée instantanée** à partir de la pression et de la géométrie du goulot
- Prise en compte de la **détente adiabatique** de l’air (\(PV^\gamma = \text{cste}\), \(\gamma = 1,4\))
- Résolution du **principe fondamental de la dynamique** (PFD) avec poids, poussée et traînée aérodynamique
- **Phase balistique** après éjection de l’eau
- Tracé des courbes : poussée, vitesse, hauteur, volume d’air
- Possibilité de modifier facilement les paramètres (masse, pression, volume d’eau, diamètre du goulot, etc.)

## Paramètres d’entrée

| Paramètre | Valeur par défaut (exemple) |
|-----------|----------------------------|
| Masse à vide (kg) | 0,33 |
| Volume d’eau (L) | 2,0 |
| Pression relative (bar) | 9,0 |
| Diamètre du goulot (mm) | 22 |
| Volume total des bouteilles (L) | 4 |
| Coefficient de traînée \(C_x\) | 0,5 |

## Bibliothèques requises

- `math` (standard)
- `matplotlib`

## Installation et exécution

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/fusee-eau.git
cd fusee-eau
