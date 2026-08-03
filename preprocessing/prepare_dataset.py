import os
import joblib
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder

# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "../data/output_bottom.csv"
OUTPUT_DIR = "../processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Chargement du dataset
# ==========================================================

print("Chargement du dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Nombre de lignes : {df.shape[0]}")
print(f"Nombre de colonnes : {df.shape[1]}")

# ==========================================================
# Suppression des colonnes inutiles
# ==========================================================

columns_to_drop = [
    "startDate",
    "endDate",
    "start",
    "end",
    "startOffset",
    "endOffset",
    "sMACs",
    "rMACs",
    "IT_B_Label",
    "IT_M_Label",
    "NST_B_Label"
]

df.drop(columns=columns_to_drop, inplace=True)

print(f"Colonnes restantes : {df.shape[1]}")

# ==========================================================
# Création du label binaire
# ==========================================================

df["Label"] = df["NST_M_Label"].apply(
    lambda x: "Normal" if x == "Normal" else "Attack"
)

df.drop(columns=["NST_M_Label"], inplace=True)

print("\nRépartition du nouveau label :")

print(df["Label"].value_counts())

# ==========================================================
# Gestion des valeurs manquantes
# ==========================================================

print("\nTraitement des valeurs manquantes...")

for column in df.columns:

    if df[column].dtype == "object":

        df[column] = df[column].fillna("Unknown")

    else:

        median = df[column].median()

        df[column] = df[column].fillna(median)

# ==========================================================
# Encodage des variables catégorielles
# ==========================================================

print("\nEncodage des variables...")

encoders = {}

categorical_columns = [
    "sAddress",
    "rAddress",
    "sIPs",
    "rIPs",
    "protocol"
]

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column].astype(str))

    encoders[column] = encoder

# ==========================================================
# Encodage du label
# ==========================================================

label_encoder = LabelEncoder()

df["Label"] = label_encoder.fit_transform(df["Label"])

encoders["Label"] = label_encoder

# ==========================================================
# Sauvegarde des encodeurs
# ==========================================================

joblib.dump(encoders, OUTPUT_DIR + "/encoders.pkl")

print("Encodeurs sauvegardés.")

# ==========================================================
# Sauvegarde du dataset
# ==========================================================

output_file = OUTPUT_DIR + "/dataset_clean.csv"

df.to_csv(output_file, index=False)

print("\nDataset sauvegardé.")

print(output_file)

print("\nTerminé.")