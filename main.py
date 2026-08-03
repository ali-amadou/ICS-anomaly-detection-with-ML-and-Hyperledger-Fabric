from pathlib import Path
import sys

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from detector.binary_detector import BinaryDetector
from blockchain.client.blockchain_client import BlockchainClient


def main():

    print("=" * 60)
    print("IA + BLOCKCHAIN FOR ICS ANOMALY DETECTION")
    print("=" * 60)

    dataset = BASE_DIR / "data" / "output_bottom.csv"

    df = pd.read_csv(dataset)

    flow = df.iloc[0].to_dict()

    detector = BinaryDetector()

    alert = detector.predict(flow)

    print("\n==========================")
    print("ALERTE")
    print("==========================")
    print(alert)

    if alert.prediction == "Attack":

        blockchain = BlockchainClient()

        tx = blockchain.submit_alert(alert)

        print("\nAlerte enregistrée dans Hyperledger Fabric")
        print("Transaction :", tx)

    else:

        print("\nFlux normal")
        print("Aucune écriture dans la blockchain.")


if __name__ == "__main__":
    main()