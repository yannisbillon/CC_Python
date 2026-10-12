
import os

import pandas as pd
import matplotlib.pyplot as plt


# 1. CHARGEMENT DES DONNÉES

FICHIER = "data/CC-AIBD-DataAnalyse-donnees (1).xlsx"

sales = pd.read_excel(
    FICHIER,
    sheet_name="Sales_data"
)

resellers = pd.read_excel(
    FICHIER,
    sheet_name="Reseller_data"
)

dates = pd.read_excel(
    FICHIER,
    sheet_name="Date_data"
)

os.makedirs("output/graphs", exist_ok=True)


# 2. FUSION VENTES / REVENDEURS

df = sales.merge(
    resellers,
    on="ResellerKey",
    how="left",
    validate="many_to_one"
)

print("=== APERÇU DES DONNÉES ===")
print(df.head())

print("\nNombre de lignes de ventes :", len(df))


# 3. FILTRAGE DES REVENDEURS NON IDENTIFIÉS

# On exclut les valeurs non renseignées et [Not Applicable]
# uniquement pour l'analyse des revendeurs.
# Le DataFrame global df reste inchangé.

noms_revendeurs = df["Reseller"].astype("string").str.strip()

masque_valides = (
    noms_revendeurs.notna()
    & noms_revendeurs.ne("[Not Applicable]")
    & noms_revendeurs.ne("")
).fillna(False)

df_revendeurs = df.loc[masque_valides].copy()

print("\n=== VÉRIFICATION DES REVENDEURS ===")
print("Lignes de ventes totales :", len(df))
print("Lignes avec revendeur identifié :", len(df_revendeurs))
print(
    "Lignes exclues des classements :",
    len(df) - len(df_revendeurs)
)

if df_revendeurs.empty:
    raise ValueError(
        "Aucun revendeur identifié après filtrage. "
        "Vérifie les valeurs de la colonne Reseller."
    )


# 4. VENTES TOTALES PAR REVENDEUR

ventes_revendeurs = (
    df_revendeurs.groupby("Reseller")["Sales Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n=== TOP 10 DES REVENDEURS IDENTIFIÉS ===")
print(ventes_revendeurs.head(10).round(2).to_string())


# 5. TOP 3

print("\n=== TOP 3 REVENDEURS POUR LA DIAPO 13 ===")

for rang, (revendeur, montant) in enumerate(
    ventes_revendeurs.head(3).items(),
    start=1
):
    print(f"{rang}. {revendeur} : {montant:,.2f} $")


# 6. GRAPHIQUE : TOP 10 DES REVENDEURS

top10 = ventes_revendeurs.head(10)

plt.figure(figsize=(12, 6))

top10.sort_values().plot(
    kind="barh",
    color="steelblue"
)

plt.title("Top 10 des revendeurs par chiffre d'affaires")
plt.xlabel("Montant des ventes ($)")
plt.ylabel("Revendeur")

plt.tight_layout()

plt.savefig(
    "output/graphs/top_revendeurs.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# 7. GRAPHIQUE : RÉPARTITION DES VENTES

# Le graphique représente uniquement les revendeurs identifiés.

top5 = ventes_revendeurs.head(5)

autres = ventes_revendeurs.iloc[5:].sum()

repartition = pd.concat([
    top5,
    pd.Series({"Autres": autres})
])

# Retirer les catégories dont le montant est nul
repartition = repartition[repartition > 0]

plt.figure(figsize=(9, 9))

plt.pie(
    repartition.values,
    labels=repartition.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Répartition des ventes des revendeurs identifiés")

plt.tight_layout()

plt.savefig(
    "output/graphs/repartition_revendeurs.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# 8. AJOUT DES DATES

# Les dates sont ajoutées au DataFrame filtré pour que
# [Not Applicable] ne réapparaisse pas dans les analyses.

df_revendeurs = df_revendeurs.merge(
    dates,
    left_on="OrderDateKey",
    right_on="DateKey",
    how="left",
    validate="many_to_one"
)

df_revendeurs["Date"] = pd.to_datetime(
    df_revendeurs["Date"],
    errors="coerce"
)

df_revendeurs["Year"] = df_revendeurs["Date"].dt.year

print("\n=== VÉRIFICATION DES DATES ===")
print(
    "Dates manquantes après fusion :",
    df_revendeurs["Date"].isna().sum()
)


# 9. VENTES ANNUELLES DES 5 PRINCIPAUX REVENDEURS

top5_noms = top5.index

df_top5 = df_revendeurs[
    df_revendeurs["Reseller"].isin(top5_noms)
].copy()

ventes_annuelles = (
    df_top5
    .dropna(subset=["Year"])
    .groupby(["Year", "Reseller"])["Sales Amount"]
    .sum()
    .unstack(fill_value=0)
    .sort_index()
)

print("\n=== VENTES ANNUELLES DES 5 PRINCIPAUX REVENDEURS ===")
print(ventes_annuelles.round(2).to_string())


# 10. GRAPHIQUE : ÉVOLUTION ANNUELLE

if not ventes_annuelles.empty:

    plt.figure(figsize=(12, 6))

    for revendeur in ventes_annuelles.columns:
        plt.plot(
            ventes_annuelles.index,
            ventes_annuelles[revendeur],
            marker="o",
            label=revendeur
        )

    plt.title(
        "Évolution annuelle des ventes des principaux revendeurs"
    )

    plt.xlabel("Année")
    plt.ylabel("Montant des ventes ($)")

    plt.xticks(ventes_annuelles.index.astype(int))

    plt.legend(
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        "output/graphs/evolution_revendeurs.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

else:
    print(
        "\nAucune donnée annuelle disponible : "
        "le graphique d'évolution n'a pas été généré."
    )


# 11. RÉSUMÉ FINAL

print("\n=== REVENDEUR LE PLUS PERFORMANT ===")

print(
    ventes_revendeurs.index[0],
    ":",
    f"{ventes_revendeurs.iloc[0]:,.2f} $"
)

print("\n=== GRAPHIQUES ENREGISTRÉS ===")
print("output/graphs/top_revendeurs.png")
print("output/graphs/repartition_revendeurs.png")

if not ventes_annuelles.empty:
    print("output/graphs/evolution_revendeurs.png")

print("\nAnalyse des revendeurs terminée.")
