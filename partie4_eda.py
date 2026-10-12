import pandas as pd
import matplotlib.pyplot as plt
import os


# 1. Chargement des données

FICHIER = "data/CC-AIBD-DataAnalyse-donnees (1).xlsx"

sales = pd.read_excel(FICHIER, sheet_name="Sales_data")
territories = pd.read_excel(FICHIER, sheet_name="Sales Territory_data")
products = pd.read_excel(FICHIER, sheet_name="Product_data")
dates = pd.read_excel(FICHIER, sheet_name="Date_data")

# Création du dossier pour les graphiques s'il n'existe pas
os.makedirs("output/graphs", exist_ok=True)


# 2. Fusion des données nécessaires

df = sales.merge(
    territories,
    on="SalesTerritoryKey",
    how="left"
)

df = df.merge(
    products,
    on="ProductKey",
    how="left"
)

df = df.merge(
    dates,
    left_on="OrderDateKey",
    right_on="DateKey",
    how="left"
)

print("=== Données fusionnées ===")
print(df.head())
print("\nNombre de lignes :", len(df))


# 3. Ventes totales par territoire

ventes_territoire = (
    df.groupby(["Country", "Region"])["Sales Amount"]
    .sum()
    .sort_values()
)

# Country + Region sur une deuxième ligne
labels = [
    f"{country}\n{region}"
    for country, region in ventes_territoire.index
]

plt.figure(figsize=(10, 6))

bars = plt.barh(
    labels,
    ventes_territoire.values
)

plt.title("Ventes totales par territoire")
plt.xlabel("Montant des ventes")
plt.ylabel("Territoire")

# Valeur au bout de chaque barre
for bar in bars:
    largeur = bar.get_width()

    plt.text(
        largeur,
        bar.get_y() + bar.get_height() / 2,
        f"{largeur:,.0f} $",
        va="center"
    )

plt.tight_layout()

plt.savefig(
    "output/graphs/ventes_par_territoire.png",
    dpi=300
)

plt.show()


# 4. Ventes totales par modèle de produit

ventes_modele = (
    df.groupby("Model")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

plt.figure(figsize=(12, 6))

ventes_modele.plot(kind="bar")

plt.title("Top 15 des modèles par ventes")
plt.xlabel("Modèle")
plt.ylabel("Montant des ventes")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    "output/graphs/ventes_par_modele.png",
    dpi=300
)

plt.show()


# 5. Ventes quotidiennes

df["Date"] = pd.to_datetime(df["Date"])

ventes_journalieres = (
    df.groupby("Date")["Sales Amount"]
    .sum()
    .sort_index()
    .to_frame()
)

# Moyennes mobiles
ventes_journalieres["Moyenne 7 jours"] = (
    ventes_journalieres["Sales Amount"]
    .rolling(window=7)
    .mean()
)

ventes_journalieres["Moyenne 30 jours"] = (
    ventes_journalieres["Sales Amount"]
    .rolling(window=30)
    .mean()
)


plt.figure(figsize=(14, 6))

plt.plot(
    ventes_journalieres.index,
    ventes_journalieres["Sales Amount"],
    label="Ventes quotidiennes"
)

plt.plot(
    ventes_journalieres.index,
    ventes_journalieres["Moyenne 7 jours"],
    label="Moyenne mobile 7 jours"
)

plt.plot(
    ventes_journalieres.index,
    ventes_journalieres["Moyenne 30 jours"],
    label="Moyenne mobile 30 jours"
)

plt.title("Évolution des ventes dans le temps")
plt.xlabel("Date")
plt.ylabel("Montant des ventes")
plt.legend()

plt.tight_layout()

plt.savefig(
    "output/graphs/evolution_ventes.png",
    dpi=300
)

plt.show()


# 6. Tableau croisé produit / territoire

tableau_croise = pd.pivot_table(
    df,
    values="Sales Amount",
    index="Model",
    columns="Country",
    aggfunc="sum",
    fill_value=0
)

print("\n=== Tableau croisé : ventes par modèle et pays ===")
print(tableau_croise)