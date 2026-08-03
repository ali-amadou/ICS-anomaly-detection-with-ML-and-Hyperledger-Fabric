from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import joblib
import pandas as pd

from preprocessing.flow_preprocessor import FlowPreprocessor
from alerts.alert import Alert
from classifier.attack_classifier import AttackClassifier
class BinaryDetector:

    def __init__(self, threshold=0.50):

        model_path = BASE_DIR / "models" / "random_forest_selected.pkl"
        feature_path = BASE_DIR / "models" / "selected_features.pkl"
        self.model = joblib.load(model_path)
        self.features = joblib.load(feature_path)

        self.threshold = threshold

        # Chargement du classificateur d'attaques
        self.attack_classifier = AttackClassifier()
        self.preprocessor = FlowPreprocessor()
        print("RandomForest_Selected_v1 chargé avec succès.")

    def predict(self, flow):

    # Sauvegarde du flux original (IP lisibles)
        original_flow = flow.copy()

    # Encodage pour le modèle IA
        encoded_flow = self.preprocessor.encode(flow)

        df = pd.DataFrame([encoded_flow])

        missing = [c for c in self.features if c not in df.columns]

        if missing:
            raise ValueError(f"Colonnes manquantes : {missing}")

        df = df[self.features]

        probabilities = self.model.predict_proba(df)[0]

        classes = self.model.classes_

        proba = dict(zip(classes, probabilities))

        attack_probability = float(proba[0])
        normal_probability = float(proba[1])

        confidence = max(attack_probability, normal_probability)

        prediction = (
            "Attack"
        if attack_probability >= self.threshold
        else "Normal"
        )

        severity = self.compute_severity(attack_probability)

        attack_type = "None"

        if prediction == "Attack":

            result = self.attack_classifier.predict(encoded_flow)

            attack_type = result["attack_type"]

        return Alert(

            timestamp=Alert.now(),

        # On utilise les vraies valeurs du flux
            source_ip=original_flow["sAddress"],

            destination_ip=original_flow["rAddress"],

            protocol=original_flow["protocol"],

            prediction=prediction,

            confidence=round(confidence, 4),

            severity=severity,

            model="RandomForest_Selected_v1",

            attack_type=attack_type,

            attack_probability=round(attack_probability, 4),

            normal_probability=round(normal_probability, 4)

    )

    def compute_severity(self, score):

        if score >= 0.90:
            return "Critical"

        elif score >= 0.75:
            return "High"

        elif score >= 0.60:
            return "Medium"

        elif score >= 0.50:
            return "Low"

        return "None"