# Analyse de données commerciales avec Python

Projet de contrôle continu consacré à l'exploration, au nettoyage, à l'analyse et à la visualisation de données de ventes.

## Objectifs

- Charger et explorer plusieurs tables de données commerciales.
- Nettoyer les valeurs manquantes et corriger les types de données.
- Analyser les ventes par produit, modèle, territoire et période.
- Étudier les statistiques descriptives et les corrélations.
- Fusionner les tables pour analyser les clients et les revendeurs.
- Produire des graphiques et formuler des recommandations commerciales.

## Technologies

- Python 3.11
- Pandas
- Matplotlib
- OpenPyXL
- pandas-stubs (aide au typage)

## Organisation du projet

```text
CC_Python/
├── .venv/                       # Environnement virtuel (non versionné)
├── data/
│   └── CC-AIBD-DataAnalyse-donnees (1).xlsx
├── output/
│   ├── graphs/                   # Graphiques PNG générés
│   └── ventes_globales.csv      # Export après fusion
├── partie1_bases_pandas.py
├── partie2_exploration.py
├── partie3_nettoyage.py
├── partie4_eda.py
├── partie5_statistiques.py
├── partie6_visualisation.py
├── partie7_temporel.py
├── partie8_fusion.py
├── partie9_revendeurs.py
├── main.py                       # Si présent dans le projet
├── requirements.txt
└── README.md
```

> Les noms des fichiers Python doivent correspondre à ceux réellement présents dans votre dossier. Le fichier Excel est nécessaire pour exécuter les scripts qui lisent les données ; certains scripts peuvent utiliser des exports CSV préparés séparément.

## Installation et lancement (PowerShell / Windows)

Ouvrir un terminal à la racine du projet, là où se trouve `requirements.txt`.

### 1. Créer un environnement virtuel si nécessaire

```powershell
python -m venv .venv
```

### 2. Activer l'environnement

```powershell
.\.venv\Scripts\Activate.ps1
```

Si le dossier `.venv` existant ne contient pas `Scripts` (par exemple s'il provient d'un autre système), créer un nouvel environnement Windows :

```powershell
python -m venv .venv_windows
.\.venv_windows\Scripts\Activate.ps1
```

### 3. Installer les dépendances

```powershell
python -m pip install -r requirements.txt
```

Exemple de contenu de `requirements.txt` :

```text
pandas
pandas-stubs
matplotlib
openpyxl
```

### 4. Exécuter les scripts

```powershell
python partie2_exploration.py
python partie3_nettoyage.py
python partie4_eda.py
python partie5_statistiques.py
python partie6_visualisation.py
python partie7_temporel.py
python partie8_fusion.py
python partie9_revendeurs.py
```

Les scripts sont organisés par thème et peuvent être lancés individuellement. Pour la partie 1 :

```powershell
python partie1_bases_pandas.py
```

## Données utilisées

Le classeur Excel contient sept feuilles :

| Feuille | DataFrame | Nombre de lignes |
|---|---|---:|
| Sales Order_data | `orders` | 121 253 |
| Sales Territory_data | `territories` | 11 |
| Sales_data | `sales` | 121 253 |
| Reseller_data | `resellers` | 702 |
| Date_data | `dates` | 1 461 |
| Product_data | `products` | 397 |
| Customer_data | `customers` | 18 485 |

Ces nombres correspondent aux données explorées pendant le projet.

## Détail des parties

| Partie | Description |
|---|---|
| 1 — Bases Pandas | Configuration de Pandas, DataFrame aléatoire, Series et Index. |
| 2 — Exploration | Chargement, `head()`, `dtypes`, `info()`, `describe()` et statistiques sur le coût standard. |
| 3 — Nettoyage | Traitement des valeurs manquantes, conversion des prix, calculs de ratios et de marges. |
| 4 — Analyse exploratoire | Chiffre d'affaires par territoire et modèle, évolution journalière et tableaux croisés. |
| 5 — Statistiques | Statistiques descriptives, corrélations et classements. |
| 6 — Visualisations | Nuages de points, boxplots, heatmap et graphiques de répartition. |
| 7 — Analyse temporelle | Agrégation des ventes par mois, trimestre et année. |
| 8 — Fusion globale | Jointures entre tables, analyses des clients et produits, export CSV. |
| 9 — Revendeurs | Classement des revendeurs identifiés, répartition et évolution annuelle. |

## Nettoyage et choix méthodologiques

- Les valeurs manquantes de `Color` sont identifiées et peuvent être remplacées par `Unknown`.
- Les prix stockés sous forme de chaînes (`$`, virgules décimales) sont convertis en valeurs numériques pour permettre les calculs.
- La marge est calculée à partir du montant des ventes et du coût total du produit : `Margin = Sales Amount - Total Product Cost`.
- Les jointures utilisent principalement `how="left"` afin de préserver les lignes de la table des ventes. Le contrôle effectué dans le projet a retrouvé **121 253 lignes avant et après fusion**.
- Pour les classements individuels des clients et des revendeurs, la valeur `[Not Applicable]` est exclue. Les ventes correspondantes restent conservées dans la vue globale.

## Graphiques et exports

Les fichiers sont générés dans `output/graphs/`, notamment :

```text
ventes_par_territoire.png
ventes_par_modele.png
evolution_ventes.png
scatter_ventes_marge.png
boxplot_territoires.png
heatmap_correlations.png
repartition_categories.png
repartition_territoires.png
ventes_mensuelles.png
ventes_trimestrielles.png
ventes_annuelles.png
top_clients_depenses.png
top_produits.png
top_revendeurs.png
repartition_revendeurs.png
evolution_revendeurs.png
```

Le script de fusion produit également :

```text
output/ventes_globales.csv
```

## Principaux résultats observés

- **121 253** lignes de ventes ont été conservées lors de la fusion vérifiée.
- La région **Southwest** représente environ **22,0 %** du chiffre d'affaires sur le graphique de répartition territoriale.
- **Southwest, Canada et Northwest** représentent ensemble environ **51,5 %** des ventes.
- La corrélation observée entre `Sales Amount` et `Margin` est d'environ **0,20**, indiquant une faible relation linéaire positive.
- La corrélation entre `Sales Amount` et `Total Product Cost` est d'environ **0,97**, indiquant une forte relation linéaire positive.

Ces constats illustrent l'intérêt de compléter l'analyse du chiffre d'affaires par une analyse des coûts et des marges.

## Pistes d'amélioration

- Approfondir l'analyse des marges par produit et par territoire.
- Renforcer les contrôles de qualité des données après chaque jointure.
- Construire un tableau de bord interactif pour faciliter l'exploration des résultats.

## Auteur

Projet réalisé dans le cadre d'un contrôle continu en analyse de données avec Python.
