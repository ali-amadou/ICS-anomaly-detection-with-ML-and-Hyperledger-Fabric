import joblib
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# ==========================================================
# Chargement du modèle
# ==========================================================

print("Chargement du modèle...")

model = joblib.load("../models/random_forest.pkl")

X_test, y_test = joblib.load("../models/test_set.pkl")

# ==========================================================
# Prédictions
# ==========================================================

print("Prédictions...")

y_pred = model.predict(X_test)

# ==========================================================
# Calcul des métriques
# ==========================================================

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n==============================")
print("Résultats")
print("==============================")

print(f"Accuracy :  {accuracy:.4f}")
print(f"Precision:  {precision:.4f}")
print(f"Recall   :  {recall:.4f}")
print(f"F1 Score :  {f1:.4f}")

print("\nClassification Report")

print(classification_report(
    y_test,
    y_pred,
    target_names=["Attack", "Normal"]
))

# ==========================================================
# Matrice de confusion
# ==========================================================

cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Attack", "Normal"]
)

disp.plot()

plt.title("Confusion Matrix")

plt.show()

# ==========================================================
# Importance des variables
# ==========================================================

print("\n==============================")
print("Top 20 des variables importantes")
print("==============================")

features = joblib.load("../models/features.pkl")

importance = model.feature_importances_

ranking = sorted(
    zip(features, importance),
    key=lambda x: x[1],
    reverse=True
)

for feature, score in ranking[:20]:
    print(f"{feature:25s} {score:.4f}")

# ==========================================================
# Graphique
# ==========================================================

top = ranking[:20]

names = [x[0] for x in top]

scores = [x[1] for x in top]

plt.figure(figsize=(10,8))

plt.barh(names[::-1], scores[::-1])

plt.title("Top 20 Feature Importances")

plt.xlabel("Importance")

plt.tight_layout()

plt.show()