import pandas as pd
import os


# ======================================================
# Configuration
# ======================================================

INPUT_FILE = "../processed/dataset_clean.csv"
OUTPUT_FILE = "../processed/dataset_selected.csv"


# ======================================================
# Chargement du dataset
# ======================================================

print("Chargement du dataset...")

df = pd.read_csv(INPUT_FILE)

print("Dimensions initiales :", df.shape)


# ======================================================
# Colonnes supprimées pour redondance
# ======================================================

redundant_features = [

    # Nombre de paquets redondant avec les octets
    "sPackets",
    "rPackets",

    # Taille max redondante avec payload max
    "sBytesMax",
    "rBytesMax",

    # Moyenne octets redondante avec payload moyen
    "rBytesAvg",

    # Variables TCP fortement corrélées
    "rttl",
    "rAckRate",

    # Délai ACK maximum redondant avec moyenne
    "sAckDelayMax"

]


# ======================================================
# Variables avec importance quasi nulle
# ======================================================

low_importance_features = [

    "sFragmentRate",
    "rFragmentRate",

    "sUrgRate",
    "rUrgRate",

    "sAckRate",
    "rRstRate"

]


# Fusion des listes

features_to_remove = (
    redundant_features +
    low_importance_features
)


# ======================================================
# Suppression sécurisée
# ======================================================

existing_features = [
    col for col in features_to_remove
    if col in df.columns
]


df.drop(
    columns=existing_features,
    inplace=True
)


# ======================================================
# Sauvegarde
# ======================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ======================================================
# Résumé
# ======================================================

print("\nColonnes supprimées :")

for col in existing_features:
    print("-", col)


print("\nNouvelle dimension :", df.shape)

print("\nDataset sauvegardé :")
print(OUTPUT_FILE)