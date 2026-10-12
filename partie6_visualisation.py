import os

import matplotlib.pyplot as plt
import pandas as pd

# 1. Chargement des données

FICHIER = "data/CC-AIBD-DataAnalyse-donnees (1).xlsx"

sales = pd.read_excel(
    FICHIER,
    sheet_name="Sales_data"
)

territories = pd.read_excel(
    FICHIER,
    sheet_name="Sales Territory_data"
)

products = pd.read_excel(
    FICHIER,
    sheet_name="Product_data"
)

os.makedirs("output/graphs", exist_ok=True)

# 2. Fusion des données

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

# 3. Calcul de la marge

df["Margin"] = (
    df["Sales Amount"]
    - df["Total Product Cost"]
)

# 4. Scatter plot : ventes / marge

plt.figure(figsize=(10, 6))

scatter = plt.scatter(
    df["Sales Amount"],
    df["Margin"],
    c=df["Unit Price"],
    alpha=0.5
)

plt.colorbar(
    scatter,
    label="Prix unitaire"
)

plt.title("Relation entre les ventes et la marge")
plt.xlabel("Montant des ventes")
plt.ylabel("Marge")

plt.tight_layout()

plt.savefig(
    "output/graphs/scatter_ventes_marge.png",
    dpi=300
)

plt.show()

# 5. Box plot des ventes par territoire

territoires = df["Region"].dropna().unique()

donnees_boxplot = [
    df.loc[
        df["Region"] == territoire,
        "Sales Amount"
    ].dropna()
    for territoire in territoires
]

plt.figure(figsize=(12, 6))

plt.boxplot(
    donnees_boxplot,
    tick_labels=territoires
)

plt.title("Distribution des ventes par territoire")
plt.xlabel("Territoire")
plt.ylabel("Montant des ventes")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "output/graphs/boxplot_territoires.png",
    dpi=300
)

plt.show()

# 6. Heatmap des corrélations

correlations = df[
    [
        "Sales Amount",
        "Total Product Cost",
        "Margin",
        "Unit Price"
    ]
].corr()

plt.figure(figsize=(8, 6))

image = plt.imshow(
    correlations,
    aspect="auto"
)

plt.colorbar(
    image,
    label="Corrélation"
)

plt.xticks(
    range(len(correlations.columns)),
    correlations.columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlations.columns)),
    correlations.columns
)

# Valeurs des corrélations dans les cases
for i in range(len(correlations)):
    for j in range(len(correlations)):
        plt.text(
            j,
            i,
            f"{correlations.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Heatmap des corrélations")

plt.tight_layout()

plt.savefig(
    "output/graphs/heatmap_correlations.png",
    dpi=300
)

plt.show()

# 7. Parts de marché par catégorie de produit

ventes_categories = (
    df.groupby("Category")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 8))

plt.pie(
    ventes_categories.values,
    labels=ventes_categories.index,
    autopct="%1.1f%%"
)

plt.title("Répartition des ventes par catégorie")

plt.tight_layout()

plt.savefig(
    "output/graphs/repartition_categories.png",
    dpi=300
)

plt.show()

# 8. Parts de marché par territoire

ventes_territoires = (
    df.groupby("Region")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 9))

plt.pie(
    ventes_territoires.values,
    labels=ventes_territoires.index,
    autopct="%1.1f%%"
)

plt.title("Répartition des ventes par territoire")

plt.tight_layout()

plt.savefig(
    "output/graphs/repartition_territoires.png",
    dpi=300
)

plt.show()


# 9. Résultats dans le terminal

print("\n=== Matrice de corrélation ===")
print(correlations.round(2))

print("\n=== Ventes par catégorie ===")
print(ventes_categories)

print("\n=== Ventes par territoire ===")
print(ventes_territoires)

print("\nTous les graphiques ont été enregistrés.")