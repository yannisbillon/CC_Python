import os

import matplotlib.pyplot as plt
import pandas as pd


# 1. Chargement des données

FICHIER = "data/CC-AIBD-DataAnalyse-donnees (1).xlsx"

sales = pd.read_excel(
    FICHIER,
    sheet_name="Sales_data"
)

dates = pd.read_excel(
    FICHIER,
    sheet_name="Date_data"
)

os.makedirs("output/graphs", exist_ok=True)


# 2. Fusion des ventes avec les dates

df = sales.merge(
    dates,
    left_on="OrderDateKey",
    right_on="DateKey",
    how="left"
)

print("=== Aperçu des données ===")
print(df.head())


# 3. Conversion de la date

df["Date"] = pd.to_datetime(df["Date"])

print("\n=== Type de la colonne Date ===")
print(df["Date"].dtype)


# 4. Utilisation de Date comme index

df = df.set_index("Date")

df = df.sort_index()


# 5. Ventes par mois

ventes_mensuelles = (
    df["Sales Amount"]
    .resample("ME")
    .sum()
)

print("\n=== Ventes mensuelles ===")
print(ventes_mensuelles)


plt.figure(figsize=(12, 6))

plt.plot(
    ventes_mensuelles.index,
    ventes_mensuelles.values,
    marker="o"
)

plt.title("Évolution mensuelle des ventes")
plt.xlabel("Date")
plt.ylabel("Montant des ventes")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/graphs/ventes_mensuelles.png",
    dpi=300
)

plt.show()

# 6. Ventes par trimestre

ventes_trimestrielles = (
    df["Sales Amount"]
    .resample("QE")
    .sum()
)

print("\n=== Ventes trimestrielles ===")
print(ventes_trimestrielles)


plt.figure(figsize=(12, 6))

plt.plot(
    ventes_trimestrielles.index,
    ventes_trimestrielles.values,
    marker="o"
)

plt.title("Évolution trimestrielle des ventes")
plt.xlabel("Date")
plt.ylabel("Montant des ventes")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "output/graphs/ventes_trimestrielles.png",
    dpi=300
)

plt.show()

# 7. Ventes par année

ventes_annuelles = (
    df["Sales Amount"]
    .resample("YE")
    .sum()
)

print("\n=== Ventes annuelles ===")
print(ventes_annuelles)


plt.figure(figsize=(10, 6))

bars = plt.bar(
    ventes_annuelles.index.year,
    ventes_annuelles.values
)

plt.title("Ventes totales par année")
plt.xlabel("Année")
plt.ylabel("Montant des ventes")

# Affichage des valeurs au-dessus des barres
for bar in bars:

    valeur = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        valeur,
        f"{valeur:,.0f} $",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "output/graphs/ventes_annuelles.png",
    dpi=300
)

plt.show()

# 8. Comparaison générale

print("\n=== Résumé ===")

print(
    "Total des ventes :",
    round(df["Sales Amount"].sum(), 2),
    "$"
)

print(
    "Meilleur mois :",
    ventes_mensuelles.idxmax().strftime("%Y-%m")
)

print(
    "Ventes du meilleur mois :",
    round(ventes_mensuelles.max(), 2),
    "$"
)

print(
    "Meilleure année :",
    ventes_annuelles.idxmax().year
)

print(
    "Ventes de la meilleure année :",
    round(ventes_annuelles.max(), 2),
    "$"
)