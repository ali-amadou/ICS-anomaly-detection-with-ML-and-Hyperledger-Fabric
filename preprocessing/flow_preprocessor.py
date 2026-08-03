from pathlib import Path
import joblib
import pandas as pd


class FlowPreprocessor:

    def __init__(self):

        BASE_DIR = Path(__file__).resolve().parent.parent

        self.encoders = joblib.load(
            BASE_DIR / "preprocessing" / "encoders.pkl"
        )

    def encode(self, flow: dict):

        """
        Encode les colonnes catégorielles avant l'IA.
        """

        encoded = flow.copy()

        categorical = [
            "sAddress",
            "rAddress",
            "sIPs",
            "rIPs",
            "protocol"
        ]

        for column in categorical:

            if column in encoded:

                encoder = self.encoders[column]["encode"]

                if encoded[column] in encoder:

                    encoded[column] = encoder[encoded[column]]

        return encoded

    def decode(self, flow: dict):

        """
        Reconstruit les vraies IP après la prédiction.
        """

        decoded = flow.copy()

        categorical = [
            "sAddress",
            "rAddress",
            "sIPs",
            "rIPs",
            "protocol"
        ]

        for column in categorical:

            if column in decoded:

                decoder = self.encoders[column]["decode"]

                if decoded[column] in decoder:

                    decoded[column] = decoder[decoded[column]]

        return decoded