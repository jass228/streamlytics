# Streamlytics

Streamlytics est un projet de pipeline ETL (Extraction, Transformation, Chargement) conçu pour analyser et explorer le catalogue Netflix à l'aide des données provenant de l'API TMDB. Ce projet vise à fournir des insights analytiques riches sur les films et séries disponibles sur Netflix, tels que les genres dominants, les scores moyens et les tendances de production.

## Caractéristiques principales

- **Extraction des données** depuis l'API TMDB sur les films et séries disponibles sur Netflix.
- **Transformation des données**: nettoyage, enrichissement, et organisation des informations clés.
- **Chargement des données** dans des bases de données :
  - **PostgreSQL** pour des analyses structurées.
  - **MongoDB** pour une flexibilité supplémentaire avec des documents JSON.
- **Rapports analytiques** sur le catalogue Netflix :
  - Répartition des genres.
  - Scores moyens des films et séries.
  - Distribution des langues et des dates de sortie.

## Technologies utilisées

- Orchestrateur : Apache Airflow
- Langage : Python
- Bases de données : PostgreSQL et MongoDB
- API : TMDB (The Movie Database)
- Bibliothèques Python :
  - pandas pour la transformation des données.
  - requests pour les appels API.
  - matplotlib et seaborn pour les visualisations.

## Installation

### 1. Prérequis

- Python 3.8 ou supérieur
- Apache Airflow 2.0 ou supérieur
- PostgreSQL (version recommandée : 13+)
- MongoDB (version recommandée : 5+)
- Compte API TMDB (obtenez une clé API depuis TMDB)

### 2. Installation des dépendances

Cloner ce dépôt et installer les dépendances requises:

```bash
git clone https://github.com/votre-utilisateur/streamlytics.git
cd streamlytics
pip install -r requirements.txt
```

### 3. Configuration

1. Configurer la base de données PostgreSQL :
   - Créez une base de données nommée streamlytics.
   - Configurez l'utilisateur et le mot de passe dans le fichier config.py.
2. Configurer MongoDB :
   - Assurez-vous que MongoDB est en cours d'exécution et configurez les détails de connexion dans config.py.
3. Ajoutez votre clé API TMDB dans le fichier .env :

```bash
TMDB_API_KEY=[votre_cle_api]
```

### 4. Démarrer Airflow

Initialisez et démarrez le scheduler et le webserver d'Airflow :

```bash
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow webserver
airflow scheduler
```

Ajoutez ensuite le DAG du pipeline ETL en copiant les fichiers dans le dossier dags/.

## Utilisation

1. Exécuter le pipeline

- Ouvrez l'interface Airflow (par défaut sur http://localhost:8080).
- Activez et déclenchez le DAG streamlytics_etl.

2. Visualiser les données

- Utilisez un outil comme pgAdmin ou Mongo Compass pour explorer les données dans PostgreSQL et MongoDB.
- Pour les rapports analytiques, exécutez les notebooks disponibles dans le dossier reports/.

## Structure du projet

```plaintext
streamlytics/
│
├── dags/               # Fichiers du pipeline ETL pour Airflow
├── data/               # Données brutes (optionnel)
├── reports/            # Notebooks pour les analyses et visualisations
├── config.py           # Configuration des bases de données et API
├── requirements.txt    # Dépendances Python
├── README.md           # Documentation du projet
└── .env                # Fichier pour les variables d'environnement
```

## Exemples de rapports analytiques

### Répartition des genres

Un graphique circulaire montrant la proportion des genres dominants dans le catalogue Netflix.

### Scores moyens par année

Une ligne temporelle illustrant l'évolution des scores moyens des contenus Netflix au fil des années.

### Distribution des langues

Un diagramme à barres représentant les langues principales utilisées dans les films et séries Netflix.

## Contributeurs

- jass228

## Licence

Ce projet est sous licence
