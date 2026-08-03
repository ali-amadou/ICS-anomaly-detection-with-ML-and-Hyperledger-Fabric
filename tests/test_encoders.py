from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

encoders = joblib.load(
    BASE_DIR / "preprocessing" / "encoders.pkl"
)

print("\n=== Encodage ===")
print(encoders["sAddress"]["encode"])

print("\n=== Décodage ===")
print(encoders["sAddress"]["decode"])