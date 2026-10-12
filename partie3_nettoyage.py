import pandas as pd

# 1. Chargement des produits

FICHIER_PRODUCTS = "data/CC-AIBD-DataAnalyse-donnees(Product_data).csv"

products = pd.read_csv(
    FICHIER_PRODUCTS,
    sep=";"
)


# 2. Recherche des valeurs manquantes

print("=== Valeurs manquantes par colonne ===")
print(products.isna().sum())


# 3. Remplacement des couleurs manquantes

products["Color"] = products["Color"].fillna("Unknown")

print("\n=== Valeurs manquantes après correction ===")
print(products.isna().sum())


# 4. Conversion de Standard Cost

products["Standard Cost"] = (
    products["Standard Cost"]
    .str.replace("$", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)


# 5. Conversion de List Price

products["List Price"] = (
    products["List Price"]
    .str.replace("$", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)


# 6. Vérification des types après nettoyage

print("\n=== Types après nettoyage ===")
print(products.dtypes)


print("\n=== Aperçu des données nettoyées ===")
print(products.head())


print("\n=== BILAN DU NETTOYAGE ===")

print("\nValeurs manquantes dans Color :")
print(products["Color"].isna().sum())
