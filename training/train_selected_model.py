import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# =====================================================
# Configuration
# =====================================================

INPUT_FILE = "../processed/dataset_selected.csv"

MODEL_DIR = "../models"

os.makedirs(MODEL_DIR, exist_ok=True)


# =====================================================
# Chargement dataset
# =====================================================

print("Chargement du dataset sélectionné...")

df = pd.read_csv(INPUT_FILE)


print("Dimensions :", df.shape)


# =====================================================
# Séparation X / y
# =====================================================

X = df.drop(columns=["Label"])

y = df["Label"]


print("\nNombre de features :", X.shape[1])


# Sauvegarde des features

joblib.dump(
    list(X.columns),
    MODEL_DIR + "/selected_features.pkl"
)


# =====================================================
# Train / Test split
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)


print("\nTrain :", X_train.shape)

print("Test :", X_test.shape)



# =====================================================
# Modèle Random Forest
# =====================================================

model = RandomForestClassifier(

    n_estimators=200,

    max_depth=20,

    random_state=42,

    n_jobs=-1,

    class_weight="balanced"

)



# =====================================================
# Entraînement
# =====================================================

print("\nEntraînement du modèle...")

model.fit(
    X_train,
    y_train
)


print("Entraînement terminé.")



# =====================================================
# Sauvegarde
# =====================================================

joblib.dump(
    model,
    MODEL_DIR + "/random_forest_selected.pkl"
)


joblib.dump(
    (X_test, y_test),
    MODEL_DIR + "/selected_test_set.pkl"
)


print("\nModèle sauvegardé :")
print("../models/random_forest_selected.pkl")