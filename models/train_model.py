import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "../processed/dataset_clean.csv"
MODEL_DIR = "../models"

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================================
# Chargement
# ==========================================================

print("Chargement du dataset...")

df = pd.read_csv(INPUT_FILE)

# ==========================================================
# Séparation Features / Label
# ==========================================================

X = df.drop(columns=["Label"])
y = df["Label"]

print(f"\nNombre de variables : {X.shape[1]}")
print(f"Nombre d'exemples : {X.shape[0]}")

# ==========================================================
# Sauvegarde de la liste des colonnes
# ==========================================================

joblib.dump(list(X.columns), MODEL_DIR + "/features.pkl")

# ==========================================================
# Découpage Train/Test
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTrain :", X_train.shape)
print("Test  :", X_test.shape)

# ==========================================================
# Création du modèle
# ==========================================================

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=20,

    random_state=42,

    n_jobs=-1,

    class_weight="balanced"
)

# ==========================================================
# Entraînement
# ==========================================================

print("\nEntraînement...")

model.fit(X_train, y_train)

print("Terminé.")

# ==========================================================
# Sauvegarde
# ==========================================================

joblib.dump(model, MODEL_DIR + "/random_forest.pkl")

joblib.dump((X_test, y_test), MODEL_DIR + "/test_set.pkl")

print("\nModèle sauvegardé.")