from pathlib import Path
import pandas as pd

from flow_preprocessor import FlowPreprocessor

BASE_DIR = Path(__file__).resolve().parent.parent

original = pd.read_csv(
    BASE_DIR / "processed" / "data_selected.csv"
)

flow = original.iloc[0].to_dict()

preprocessor = FlowPreprocessor()

encoded = preprocessor.encode(flow)

decoded = preprocessor.decode(encoded)

print("\n===== ORIGINAL =====")
print(flow["sAddress"], flow["rAddress"], flow["protocol"])

print("\n===== ENCODED =====")
print(encoded["sAddress"], encoded["rAddress"], encoded["protocol"])

print("\n===== DECODED =====")
print(decoded["sAddress"], decoded["rAddress"], decoded["protocol"])