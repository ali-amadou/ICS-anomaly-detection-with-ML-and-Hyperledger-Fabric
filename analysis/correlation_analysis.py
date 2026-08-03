import pandas as pd
import matplotlib.pyplot as plt

# =======================================
# Chargement
# =======================================

df = pd.read_csv("../processed/dataset_clean.csv")

# On retire le label
X = df.drop(columns=["Label"])

# =======================================
# Corrélation
# =======================================

corr = X.corr(numeric_only=True)

# Sauvegarde de la matrice

corr.to_csv("../processed/correlation_matrix.csv")

# =======================================
# Recherche automatique
# =======================================

threshold = 0.95

print("="*60)
print("Variables fortement corrélées")
print("="*60)

already_seen = set()

for i in range(len(corr.columns)):

    for j in range(i+1, len(corr.columns)):

        c = corr.iloc[i, j]

        if abs(c) >= threshold:

            col1 = corr.columns[i]
            col2 = corr.columns[j]

            print(f"{col1:25s} <--> {col2:25s} : {c:.3f}")