import json
import socket
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from detector.binary_detector import BinaryDetector
from blockchain.client.blockchain_client import BlockchainClient


HOST = "0.0.0.0"
PORT = 5000


def start_receiver():

    print("=" * 60)
    print("ICS REAL-TIME FLOW RECEIVER")
    print("=" * 60)
    print(f"Listening on {HOST}:{PORT}")

    detector = BinaryDetector()
    blockchain = BlockchainClient()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen(1)

    print("Waiting for PC 2...")

    conn, address = server.accept()

    print(f"Connected: {address}")

    buffer = ""

    try:

        while True:

            data = conn.recv(4096)

            if not data:
                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:

                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

                try:

                    flow = json.loads(line)

                    print("\nFlow received")

                    alert = detector.predict(flow)

                    print(
                        f"Prediction: {alert.prediction} | "
                        f"Confidence: {alert.confidence} | "
                        f"Severity: {alert.severity}"
                    )

                    if alert.prediction == "Attack":

                        print("ATTACK DETECTED")
                        print(f"Attack Type: {alert.attack_type}")
                        alert_id = blockchain.submit_alert(alert)

                        print(
                            f"Blockchain alert ID: {alert_id}"
                        )

                except Exception as e:

                    print(f"Error processing flow: {e}")

    except KeyboardInterrupt:

        print("\nStopping receiver...")

    finally:

        conn.close()
        server.close()


if __name__ == "__main__":
    start_receiver()