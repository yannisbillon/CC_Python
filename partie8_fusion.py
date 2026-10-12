
import os

import matplotlib.pyplot as plt
import pandas as pd


# 1. CHARGEMENT DES DONNÉES

FICHIER = "data/CC-AIBD-DataAnalyse-donnees (1).xlsx"

sales = pd.read_excel(FICHIER, sheet_name="Sales_data")
products = pd.read_excel(FICHIER, sheet_name="Product_data")
territories = pd.read_excel(FICHIER, sheet_name="Sales Territory_data")
customers = pd.read_excel(FICHIER, sheet_name="Customer_data")
dates = pd.read_excel(FICHIER, sheet_name="Date_data")
orders = pd.read_excel(FICHIER, sheet_name="Sales Order_data")

os.makedirs("output/graphs", exist_ok=True)


# 2. NOMBRE DE LIGNES AVANT FUSION

nombre_ventes_avant = len(sales)

print("=== Nombre de ventes avant fusion ===")
print(nombre_ventes_avant)


# 3. FUSION GLOBALE DES TABLES

df = sales.merge(
    products,
    on="ProductKey",
    how="left"
)

df = df.merge(
    territories,
    on="SalesTerritoryKey",
    how="left"
)

df = df.merge(
    orders,
    on="SalesOrderLineKey",
    how="left"
)

df = df.merge(
    customers,
    on="CustomerKey",
    how="left"
)

df = df.merge(
    dates,
    left_on="OrderDateKey",
    right_on="DateKey",
    how="left"
)


# 4. VÉRIFICATION DE LA FUSION

nombre_ventes_apres = len(df)

print("\n=== Vérification de la fusion ===")
print("Avant :", nombre_ventes_avant)
print("Après :", nombre_ventes_apres)

if nombre_ventes_avant == nombre_ventes_apres:
    print("OK : le nombre de lignes de ventes est conservé.")
else:
    print("ATTENTION : le nombre de lignes a changé.")

print("\n=== Dimensions du DataFrame global ===")
print(df.shape)

print("\n=== Aperçu ===")
print(df.head())


# 5. VENTES PAR PRODUIT ET TERRITOIRE

ventes_produit_territoire = (
    df.groupby(["Country", "Region", "Product"])["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n=== Ventes par produit et territoire ===")
print(ventes_produit_territoire.head(20))


# 6. NOMBRE DE PRODUITS PAR MODÈLE

produits_par_modele = (
    products.groupby("Model")["ProductKey"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n=== Nombre de produits par modèle ===")
print(produits_par_modele)


# 7. PRÉPARATION DES DONNÉES CLIENTS

# On exclut les clients non identifiés UNIQUEMENT
# pour les classements de clients.
#
# Le DataFrame global "df" reste inchangé.

noms_clients = df["Customer"].astype("string").str.strip()

masque_clients_valides = (
    noms_clients.notna()
    & noms_clients.ne("[Not Applicable]")
    & noms_clients.ne("")
)

clients_valides = df.loc[masque_clients_valides].copy()

print("\n=== Vérification des clients ===")
print("Lignes de ventes totales :", len(df))
print("Lignes avec client identifié :", len(clients_valides))
print(
    "Lignes exclues des classements clients :",
    len(df) - len(clients_valides)
)


# 8. TOP 10 CLIENTS PAR NOMBRE DE COMMANDES

commandes_clients = (
    clients_valides.groupby("Customer")["Sales Order"]
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)

print("\n=== Top 10 clients par nombre de commandes ===")
print(commandes_clients.to_string())


# 9. TOP 10 CLIENTS PAR MONTANT DÉPENSÉ

depenses_clients = (
    clients_valides.groupby("Customer")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n=== Top 10 clients par montant dépensé ===")
print(depenses_clients.round(2).to_string())


# 10. TOP 3 CLIENTS POUR LA PRÉSENTATION

print("\n=== TOP 3 CLIENTS POUR LA DIAPO 12 ===")

for rang, (client, montant) in enumerate(
    depenses_clients.head(3).items(),
    start=1
):
    print(f"{rang}. {client} : {montant:,.2f} $")


# 11. NOMBRE DE VENTES PAR CATÉGORIE ET TERRITOIRE

ventes_categorie_territoire = pd.pivot_table(
    df,
    values="Sales Amount",
    index="Category",
    columns="Region",
    aggfunc="count",
    fill_value=0
)

print("\n=== Nombre de ventes par catégorie et territoire ===")
print(ventes_categorie_territoire)


# 12. GRAPHIQUE : TOP 10 DES CLIENTS

plt.figure(figsize=(11, 6))

depenses_clients.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Top 10 des clients par montant dépensé")
plt.xlabel("Montant total des ventes ($)")
plt.ylabel("Client")

plt.tight_layout()

plt.savefig(
    "output/graphs/top_clients_depenses.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# 13. GRAPHIQUE : TOP 10 DES PRODUITS

top_produits = (
    df.groupby("Product")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n=== Top 10 produits par chiffre d'affaires ===")
print(top_produits.round(2).to_string())

plt.figure(figsize=(11, 6))

top_produits.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Top 10 des produits par chiffre d'affaires")
plt.xlabel("Montant des ventes ($)")
plt.ylabel("Produit")

plt.tight_layout()

plt.savefig(
    "output/graphs/top_produits.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# 14. SAUVEGARDE DE LA VUE GLOBALE

df.to_csv(
    "output/ventes_globales.csv",
    index=False
)

print("\n=== EXPORT TERMINÉ ===")
print("Vue globale enregistrée dans :")
print("output/ventes_globales.csv")

print("\nGraphiques enregistrés :")
print("output/graphs/top_clients_depenses.png")
print("output/graphs/top_produits.png")
