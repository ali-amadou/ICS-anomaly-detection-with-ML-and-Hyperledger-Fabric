from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


# ============================================================
# Fichiers
# ============================================================

DATASET = BASE_DIR / "processed" / "attack_dataset.csv"

MODEL_PATH = BASE_DIR / "models" / "attack_classifier.pkl"

FEATURES_PATH = BASE_DIR / "models" / "attack_features.pkl"

ENCODER_PATH = BASE_DIR / "models" / "attack_label_encoder.pkl"

OUTPUT = BASE_DIR / "images" / "attack_confusion_matrix.png"


# ============================================================
# Chargement
# ============================================================

print("=" * 60)
print("EVALUATION DU CLASSIFICATEUR MULTICLASSES")
print("=" * 60)

print("\nChargement du dataset...")

df = pd.read_csv(DATASET)

print("Dimensions :", df.shape)


# ============================================================
# Chargement du modèle et des paramètres
# ============================================================

model = joblib.load(MODEL_PATH)

features = joblib.load(FEATURES_PATH)

encoder = joblib.load(ENCODER_PATH)

print("\nClasses du classificateur :")

for i, label in enumerate(encoder.classes_):
    print(i, "->", label)


# ============================================================
# X / y
# ============================================================

X = df[features]

y = encoder.transform(df["AttackType"])


print("\nNombre de features :", X.shape[1])

print("Nombre total de flux :", len(X))


# ============================================================
# Même séparation que pendant l'entraînement
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


print("\nJeu d'entraînement :", X_train.shape)

print("Jeu de test :", X_test.shape)


# ============================================================
# Prédiction
# ============================================================

print("\nPrédiction sur le jeu de test...")

y_pred = model.predict(X_test)


# ============================================================
# Accuracy
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("RESULTATS")
print("=" * 60)

print("\nAccuracy :", round(accuracy, 4))

print("Accuracy :", round(accuracy * 100, 2), "%")


# ============================================================
# Classification report
# ============================================================

print("\nClassification Report :\n")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=encoder.classes_,
        digits=4
    )
)


# ============================================================
# Matrice de confusion
# ============================================================

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nMatrice de confusion :")

print(cm)


# ============================================================
# Graphique
# ============================================================

disp = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=encoder.classes_
)

disp.plot()

plt.title(
    "Matrice de confusion - Attack Classifier"
)

plt.xlabel(
    "Classe prédite"
)

plt.ylabel(
    "Classe réelle"
)

plt.tight_layout()

plt.savefig(
    OUTPUT,
    dpi=300,
    bbox_inches="tight"
)

plt.show()


print("\nMatrice sauvegardée :")

print(OUTPUT)