from pathlib import Path

import pandas as pd

from detector.binary_detector import BinaryDetector

from blockchain.client.blockchain_client import BlockchainClient


BASE_DIR = Path(__file__).resolve().parent.parent.parent

dataset = BASE_DIR / "data" / "output_bottom.csv"

df = pd.read_csv(dataset)

flow = df[df["Label"] == 0].drop(columns=["Label"]).iloc[0].to_dict()

detector = BinaryDetector()

alert = detector.predict(flow)

client = BlockchainClient()

tx = client.submit_alert(alert)

print()

print("Transaction envoyée")

print(tx)