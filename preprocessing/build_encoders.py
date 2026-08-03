from pathlib import Path
import pandas as pd
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

# Dataset original (non encodé)
original = pd.read_csv(BASE_DIR / "data" / "output_bottom.csv")

# Dataset utilisé pour entraîner l'IA (encodé)
encoded = pd.read_csv(BASE_DIR / "processed" / "dataset_selected.csv")

# Colonnes catégorielles
categorical_columns = [
    "sAddress",
    "rAddress",
    "sIPs",
    "rIPs",
    "protocol"
]

encoders = {}

for column in categorical_columns:

    print(f"Construction de l'encodeur : {column}")

    mapping = {}

    original_values = original[column].reset_index(drop=True)
    encoded_values = encoded[column].reset_index(drop=True)

    for orig, enc in zip(original_values, encoded_values):
        mapping[orig] = enc

    reverse_mapping = {v: k for k, v in mapping.items()}

    encoders[column] = {
        "encode": mapping,
        "decode": reverse_mapping
    }

joblib.dump(
    encoders,
    BASE_DIR / "preprocessing" / "encoders.pkl"
)

print("\nEncodeurs sauvegardés.")