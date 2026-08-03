from pathlib import Path
import joblib
import pandas as pd


features = joblib.load("C:\\Users\\hp\\Desktop\\Project IA+Blockchain for ICS Anomaly\\models\\selected_features.pkl")

df = pd.read_csv("C:\\Users\\hp\\Desktop\\Project IA+Blockchain for ICS Anomaly\\processed\\dataset_selected.csv")

print("Nombre de features :", len(features))
print("Nombre de colonnes du dataset (sans Label) :", len(df.columns) - 1)

missing = [f for f in features if f not in df.columns]

print("\nFeatures manquantes :")
print(missing)

extra = [c for c in df.columns if c != "Label" and c not in features]

print("\nColonnes supplémentaires :")
print(extra)