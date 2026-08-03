from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Alert:

    timestamp: str

    source_ip: str

    destination_ip: str

    protocol: str

    prediction: str

    confidence: float

    severity: str

    model: str

    attack_type: str = "Unknown"

    attack_probability: float = 0.0

    normal_probability: float = 0.0

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def now():
        return datetime.now().isoformat()