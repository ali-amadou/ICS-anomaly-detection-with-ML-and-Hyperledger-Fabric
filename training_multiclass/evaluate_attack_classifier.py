from pathlib import Path
import joblib
import pandas as pd

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Chargement
# ==========================

model = joblib.load(
    BASE_DIR / "models" / "attack_classifier.pkl"
)

encoder = joblib.load(
    BASE_DIR / "models" / "attack_label_encoder.pkl"
)

features = joblib.load(
    BASE_DIR / "models" / "attack_features.pkl"
)

dataset = pd.read_csv(
    BASE_DIR / "processed" / "attack_dataset.csv"
)

X = dataset[features]

y = encoder.transform(dataset["AttackType"])

# ==========================
# Prédictions
# ==========================

pred = model.predict(X)

print("\nAccuracy :")

print(accuracy_score(y, pred))

print("\nClassification Report\n")

print(classification_report(
    y,
    pred,
    target_names=encoder.classes_
))

print("\nMatrice de confusion\n")

print(confusion_matrix(y, pred))

# ==========================
# Importance des variables
# ==========================

importance = pd.DataFrame({

    "Feature": features,

    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 20 variables\n")

print(importance.head(20))