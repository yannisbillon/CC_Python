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

print("=== Aperçu des données ===")
print(df.head())

print("\nNombre de lignes :", len(df))


# 3. Statistiques des ventes par territoire

stats_territoires = (
    df.groupby(["Country", "Region"])["Sales Amount"]
    .agg(
        moyenne="mean",
        mediane="median",
        ecart_type="std",
        minimum="min",
        maximum="max",
        Q1=lambda x: x.quantile(0.25),
        Q3=lambda x: x.quantile(0.75)
    )
)

print("\n=== Statistiques des ventes par territoire ===")
print(stats_territoires.round(2))


# 4. Création de la marge

df["Margin"] = (
    df["Sales Amount"]
    - df["Total Product Cost"]
)

print("\n=== Exemple de calcul de marge ===")

print(
    df[
        [
            "Sales Amount",
            "Total Product Cost",
            "Margin"
        ]
    ].head()
)


# 5. Corrélation ventes / marge

correlation_sales_margin = (
    df["Sales Amount"]
    .corr(df["Margin"])
)

print("\n=== Corrélation ventes / marge ===")

print(
    round(correlation_sales_margin, 4)
)


# 6. Corrélation coût total / marge

correlation_cost_margin = (
    df["Total Product Cost"]
    .corr(df["Margin"])
)

print("\n=== Corrélation coût total / marge ===")

print(
    round(correlation_cost_margin, 4)
)


# 7. Matrice de corrélation

correlations = df[
    [
        "Sales Amount",
        "Total Product Cost",
        "Margin"
    ]
].corr()

print("\n=== Matrice de corrélation ===")
print(correlations.round(4))


# 8. Territoires avec le plus de ventes

top_territoires = (
    df.groupby(["Country", "Region"])["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n=== Territoires avec le plus de ventes ===")
print(top_territoires)


# 9. Produits avec le plus de ventes

top_produits = (
    df.groupby("Product")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n=== Top 10 produits par ventes ===")
print(top_produits)