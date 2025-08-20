# 🪐 Simulation de Collisions et Fragmentation de Particules

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green?logo=pygame&logoColor=white)
![Status](https://img.shields.io/badge/status-en%20développement-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## Description

Ce projet est une simulation physique 2D de collisions entre particules.  
Lorsqu’une collision dépasse un certain seuil d’énergie, les particules peuvent **se fragmenter** en sous-particules projetées avec des vitesses et masses calculées.  

Caractéristiques principales :
- Détection des collisions entre particules ⚡
- Calcul de l’énergie de collision 🔥
- Fragmentation en plusieurs morceaux avec conservation de la masse 💥
- Mise à jour des rayons en fonction de la masse 📏
- Visualisation avec **Pygame** 🎮

---

## Installation

Clone le projet :

```bash
git clone https://github.com/ton-compte/nom-du-projet.git
cd particle-simulation
```

Installe les dépendances : 
```bash
pip install -r requirements.txt
```

##  Utilisation
Lancer la simulation :
```bash
python main.py
```
Les particules sont générées et évoluent automatiquement.

## ⚙️ Paramètres
Les principaux paramètres se trouvent dans constants.py :

- `E_seuil` : énergie minimale pour déclencher une fragmentation.
- `c_N, beta` : paramètres de la loi de fragmentation.
- `density` : densité des particules (impacte le rayon après fragmentation).

## Structure du projet
```bash
simulation/
├── physics/
│   ├── particle.py       # Classe Particule
│   ├── collision.py      # Gestion des collisions
│   └── fragmentation.py  # Logique de fragmentation
├── main.py               # Boucle principale Pygame
├── config.py             # Paramètres globaux
└── README.md             # Documentation
```

## Licence
Ce projet est distribué sous licence MIT.  
Voir [LICENSE](https://github.com/nathan-004/particle-simulation/blob/main/LICENSE)