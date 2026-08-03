from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

dataset = BASE_DIR / "processed" / "dataset_selected.csv"

df = pd.read_csv(dataset)

print("Dataset initial :", df.shape)

# On conserve uniquement les attaques
df = df[df["Label"] == 0]

print("Attaques uniquement :", df.shape)

# Les labels proviennent du dataset original
# Ajouter les labels originaux
original = pd.read_csv(BASE_DIR / "data" / "output_bottom.csv")

original = original.loc[df.index]

df["AttackType"] = original["NST_M_Label"]

# Fusion des deux variantes Portscan
df["AttackType"] = df["AttackType"].replace({
    "BAD-PORTSCAN1": "BAD-PORTSCAN",
    "BAD-PORTSCAN2": "BAD-PORTSCAN"
})

# Suppression de GOOD-SSH
df = df[df["AttackType"] != "GOOD-SSH"]

print("\nRépartition finale")

print(df["AttackType"].value_counts())

output = BASE_DIR / "processed" / "attack_dataset.csv"

df.to_csv(output, index=False)

print("\nDataset sauvegardé :", output)