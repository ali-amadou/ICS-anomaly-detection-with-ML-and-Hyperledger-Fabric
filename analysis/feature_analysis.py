import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier

# ===========================
# Chargement
# ===========================

df = pd.read_csv("../processed/dataset_clean.csv")

X = df.drop(columns=["Label"])
y = df["Label"]

# ===========================
# Entraînement rapide
# ===========================

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf.fit(X, y)

# ===========================
# Importance
# ===========================

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance)

# ===========================
# Sauvegarde
# ===========================

importance.to_csv(
    "../processed/feature_importance.csv",
    index=False
)

# ===========================
# Graphique
# ===========================

top20 = importance.head(20)

plt.figure(figsize=(10,8))

plt.barh(
    top20["Feature"][::-1],
    top20["Importance"][::-1]
)

plt.title("Top 20 Feature Importance")

plt.tight_layout()

plt.show()