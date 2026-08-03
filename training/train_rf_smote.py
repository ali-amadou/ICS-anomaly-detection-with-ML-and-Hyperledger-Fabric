import os
import time
import joblib
import pandas as pd

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# ======================================================
# Configuration
# ======================================================

INPUT_FILE = "../processed/dataset_selected.csv"

MODEL_DIR = "../models"

os.makedirs(MODEL_DIR, exist_ok=True)

# ======================================================
# Chargement
# ======================================================

print("Chargement du dataset...")

df = pd.read_csv(INPUT_FILE)

X = df.drop(columns=["Label"])
y = df["Label"]

print("\nRépartition AVANT SMOTE :")
print(y.value_counts())

# ======================================================
# Découpage Train/Test
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ======================================================
# Application de SMOTE UNIQUEMENT sur Train
# ======================================================

print("\nApplication de SMOTE...")

smote = SMOTE(
    random_state=42,
    k_neighbors=5
)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("\nRépartition APRÈS SMOTE :")
print(y_train_smote.value_counts())

# ======================================================
# Random Forest
# ======================================================

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)

print("\nEntraînement...")

start = time.time()

model.fit(
    X_train_smote,
    y_train_smote
)

end = time.time()

print(f"Temps d'entraînement : {end-start:.2f} secondes")

# ======================================================
# Sauvegarde
# ======================================================

joblib.dump(
    model,
    "../models/random_forest_smote.pkl"
)

joblib.dump(
    (X_test, y_test),
    "../models/test_set_smote.pkl"
)

joblib.dump(
    list(X.columns),
    "../models/features_smote.pkl"
)

print("\nModèle sauvegardé.")