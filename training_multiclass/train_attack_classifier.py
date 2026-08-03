from pathlib import Path
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Chargement du dataset
# ==========================

dataset = BASE_DIR / "processed" / "attack_dataset.csv"

df = pd.read_csv(dataset)

print("Dataset :", df.shape)

# ==========================
# Variables
# ==========================

X = df.drop(columns=["Label", "AttackType"])

y = df["AttackType"]

# ==========================
# Encodage des labels
# ==========================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y)

print("\nClasses :")

for i, c in enumerate(label_encoder.classes_):
    print(i, "->", c)

# ==========================
# Séparation
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ==========================
# Modèle
# ==========================

clf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

print("\nEntraînement...")

clf.fit(X_train, y_train)

print("Terminé.")

# ==========================
# Evaluation rapide
# ==========================

pred = clf.predict(X_test)

print("\nClassification Report\n")

print(classification_report(
    y_test,
    pred,
    target_names=label_encoder.classes_
))

# ==========================
# Sauvegarde
# ==========================

joblib.dump(
    clf,
    BASE_DIR / "models" / "attack_classifier.pkl"
)

joblib.dump(
    label_encoder,
    BASE_DIR / "models" / "attack_label_encoder.pkl"
)

print("\nModèle sauvegardé.")

joblib.dump(
    list(X.columns),
    BASE_DIR / "models" / "attack_features.pkl"
)

print("Features sauvegardées.")