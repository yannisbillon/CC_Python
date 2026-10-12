import pandas as pd

# 1. Chargement des données

FICHIER_PRODUCTS = "data/CC-AIBD-DataAnalyse-donnees(Product_data).csv"

products = pd.read_csv(
    FICHIER_PRODUCTS,
    sep=";"
)


# 2. Exploration des données

print("=== 5 premières lignes ===")
print(products.head())


print("\n=== Types des colonnes ===")
print(products.dtypes)


print("\n=== Informations générales ===")
products.info()


print("\n=== Statistiques descriptives ===")
print(products.describe(include="all"))


# 3. Identification des types incorrects

print("\n=== Colonnes avec un type à corriger ===")
print("Standard Cost :", products["Standard Cost"].dtype)
print("List Price :", products["List Price"].dtype)

# Standard Cost et List Price sont lus comme du texte
# à cause du symbole $ et de la virgule décimale.


# 4. Conversion du coût standard

products["Standard Cost Numeric"] = (
    products["Standard Cost"]
    .str.replace("$", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)


print("\n=== Vérification de la conversion ===")
print(
    products[
        ["Standard Cost", "Standard Cost Numeric"]
    ].head()
)


# 5. Statistiques du coût standard

median_cost = products["Standard Cost Numeric"].median()
std_cost = products["Standard Cost Numeric"].std()
variance_cost = products["Standard Cost Numeric"].var()


print("\n=== Statistiques du coût standard ===")
print(f"Médiane : {median_cost:.2f} $")
print(f"Écart-type : {std_cost:.2f} $")
print(f"Variance : {variance_cost:.2f}")


# 6. Statistiques par catégorie
stats_category = (
    products
    .groupby("Category")["Standard Cost Numeric"]
    .agg(["median", "std", "var"])
)


print("\n=== Statistiques du coût standard par catégorie ===")
print(stats_category)

# 7. Dimensions des tables du classeur Excel

from pathlib import Path

print("\n=== TABLES CHARGÉES ===")

fichiers_excel = list(Path("data").glob("*.xlsx"))

if not fichiers_excel:
    print("Aucun fichier Excel trouvé dans data/")
else:
    fichier_excel = fichiers_excel[0]

    tables = {
        "orders": "Sales Order_data",
        "territories": "Sales Territory_data",
        "sales": "Sales_data",
        "resellers": "Reseller_data",
        "dates": "Date_data",
        "products": "Product_data",
        "customers": "Customer_data"
    }

    for nom, feuille in tables.items():
        df = pd.read_excel(fichier_excel, sheet_name=feuille)
        print(
            f"{nom:<12} → {len(df):>7,} lignes x "
            f"{df.shape[1]} colonnes"
        )