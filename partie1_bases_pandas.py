import pandas as pd
import numpy as np


# Configuration de l'affichage Pandas
pd.set_option("display.min_rows", 6)
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 12)
pd.set_option("display.max_colwidth", 20)
pd.set_option("display.width", 240)


# Création d'un DataFrame aléatoire de 200 lignes et 20 colonnes
data = np.random.rand(200, 20)

df = pd.DataFrame(
    data,
    columns=[f"Colonne_{i}" for i in range(1, 21)]
)


print("=== DataFrame de test ===")
print(df)

print("\n=== Dimensions du DataFrame ===")
print(df.shape)


# Exemple d'une Series
print("\n=== Exemple de Series ===")
print(df["Colonne_1"])


# Exemple de l'Index
print("\n=== Index du DataFrame ===")
print(df.index)