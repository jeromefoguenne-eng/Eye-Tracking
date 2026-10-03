# Projet de Recherche Eye Tracking (Lab-DRA / HECh - HEL)

[![Status](https://img.shields.io/badge/Status-En%20D%C3%A9veloppement-blue.svg)](#)
[![Hardware](https://img.shields.io/badge/Hardware-Pupil%20Labs%20Neon-green.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](#)

Ce dépôt héberge l'ensemble des travaux, analyses de données, scripts de traitement et documentations scientifiques liés au **projet de recherche en Oculométrie (Eye Tracking)** mené dans le cadre du **Lab-DRA** (Haute École Charlemagne / Haute École de la Ville de Liège).

---

## 🎯 Objectifs du Projet

1. **Analyse de l'Attention Visuelle en Situation Réelle** : Mesurer et modéliser le comportement oculomoteur (fixations, saccades, clignements, zones d'intérêt - AOI) lors de tâches didactiques, professionnelles et interactives.
2. **Technopédagogie & Révélation des Savoirs Cachés** :
   - Analyser le regard d'experts vs novices lors de mises en situation métier (scénarios pratiques, accueil, simulation).
   - Exploiter les flux vidéo avec point de regard incrusté (*gaze overlay*) pour concevoir des séquences d'apprentissage enrichies.
3. **Méthodologie & Traitement de Données** :
   - Mise en place d'un pipeline reproductible d'extraction, filtrage et visualisation des données oculométriques brutes.
   - Calcul d'indicateurs quantitatifs : durées moyennes de fixation, fréquence des saccades, cartes de chaleur (*heatmaps*), parcours visuels (*scanpaths*).

---

## 🔬 Matériel & Dispositif Expérimental

* **Capteur Oculométrique** : Lunettes **Pupil Labs Neon** (Neon Sensor Module v1).
  * Fréquence d'échantillonnage du regard : **200 Hz** (mode binoculaire).
  * Caméra de scène haute résolution avec compensation inertielle (IMU intégrée).
* **Logiciels & Acquisition** :
  * Application mobile **Neon Companion** pour l'enregistrement temps réel in-situ.
  * **Neon Player** pour la relecture et le contrôle qualité des enregistrements.
  * Pipelines d'analyse en Python (SciPy, Pandas, Matplotlib, OpenCV).

---

## 📂 Architecture du Projet

```text
Eye-Tracking/
├── data/
│   ├── raw/               # Données brutes (exclues du suivi Git pour préserver l'espace)
│   └── processed/         # Données nettoyées, métriques et extraits tabulaires (CSV/Parquet)
├── docs/
│   ├── etat_de_l_art.md   # Revue de littérature et état de l'art scientifique
│   ├── methodologie.md    # Protocoles expérimentaux, passation et éthique
│   └── architecture.md    # Description des formats de données Pupil Labs
├── notebooks/             # Carnets Jupyter pour l'analyse exploratoire et les heatmaps
├── scripts/
│   └── sync_project.py    # Script d'automatisation des sauvegardes et push Git
├── src/
│   ├── __init__.py
│   ├── loader.py          # Chargement et validation des sessions d'enregistrement Neon
│   └── metrics.py         # Calcul des métriques oculométriques (fixations, clignements)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Prise en Main Rapide

### 1. Installation de l'environnement

```bash
# Cloner le dépôt (si non déjà fait)
git clone https://github.com/jeromefoguenne-eng/Eye-Tracking.git
cd Eye-Tracking

# Créer un environnement virtuel (recommandé)
python -m venv venv
# Activer sous Windows :
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Synchronisation automatique des avancées

Pour sauvegarder et synchroniser automatiquement toutes vos avancées sur GitHub :
```bash
python scripts/sync_project.py
```

---

## 👥 Équipe & Partenariats

* **Porteur de projet** : Jérôme Foguenne (HECh / HEL)
* **Cadre institutionnel** : Lab-DRA (Projet recherche 2026-2027)
* **Collaborations de recherche** : Bernard Cornélis, Steve Gillet, Adeline Struvay, Julien Danthinne.
