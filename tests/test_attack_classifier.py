from pathlib import Path

import pandas as pd

from attack_classifier import AttackClassifier

BASE_DIR = Path(__file__).resolve().parent.parent

dataset = BASE_DIR / "processed" / "attack_dataset.csv"

df = pd.read_csv(dataset)

flow = df.drop(columns=["Label", "AttackType"]).iloc[0].to_dict()

classifier = AttackClassifier()

result = classifier.predict(flow)

print()

print("======================")

print(result)

print("======================")