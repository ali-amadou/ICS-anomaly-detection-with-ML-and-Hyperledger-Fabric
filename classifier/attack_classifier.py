from pathlib import Path

import joblib
import pandas as pd


class AttackClassifier:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.model = joblib.load(
            BASE_DIR / "models" / "attack_classifier.pkl"
        )

        self.features = joblib.load(
            BASE_DIR / "models" / "attack_features.pkl"
        )

        self.encoder = joblib.load(
            BASE_DIR / "models" / "attack_label_encoder.pkl"
        )

        print("AttackClassifier chargé.")

    def predict(self, flow):

        df = pd.DataFrame([flow])

        missing = [
            c for c in self.features
            if c not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Colonnes manquantes : {missing}"
            )

        df = df[self.features]

        probabilities = self.model.predict_proba(df)[0]

        prediction = self.model.predict(df)[0]

        attack_type = self.encoder.inverse_transform(
            [prediction]
        )[0]

        confidence = probabilities[prediction]

        return {

            "attack_type": attack_type,

            "confidence": round(float(confidence), 4)

        }