# AI-Based ICS Network Anomaly Detection with Machine Learning and Hyperledger Fabric

## Overview

This project implements an intelligent intrusion detection system for Industrial Control Systems (ICS) networks by combining Machine Learning techniques with Blockchain technology.

The objective is to detect abnormal network flows, identify cyber attacks, generate security alerts, and store these alerts in an immutable Hyperledger Fabric blockchain ledger.

The system combines:

- Machine Learning based intrusion detection
- Attack classification
- Automated alert generation
- Blockchain-based alert storage
- Future visualization through a monitoring dashboard

---

## System Architecture

The global pipeline is:

```text
ICS Network Traffic
        │
        ▼
Data Preprocessing
        │
        ▼
Machine Learning Detection
        │
        ▼
Attack Classification
        │
        ▼
Alert Generation
        │
        ▼
Hyperledger Fabric Blockchain
        │
        ▼
Security Dashboard
```

---

## Machine Learning Component

### Binary Attack Detection

A Random Forest model is used as the main detector.

**Model:** `RandomForest_Selected_v1`

The model classifies network flows into:

- Normal traffic
- Attack traffic

### Attack Classification

When malicious traffic is detected, a second classifier determines the attack category.

**Component:** `AttackClassifier`

The classifier provides:

- Attack type
- Confidence score

---

## Alert Generation

Each detected event is converted into a structured alert containing:

- Alert ID
- Timestamp
- Source IP
- Destination IP
- Protocol
- Prediction
- Attack type
- Severity level
- Confidence score
- Detection model

**Example:**

```json
{
  "alertId": "ALERT001",
  "prediction": "Attack",
  "attack_type": "BAD-MITM",
  "severity": "Critical",
  "confidence": 1.0,
  "model": "RandomForest_Selected_v1"
}
```

---

## Blockchain Layer

The blockchain component is implemented using:

- Hyperledger Fabric
- Node.js Chaincode
- Fabric Contract API

The smart contract provides:

- Alert creation
- Alert retrieval
- Alert history storage

**Blockchain advantages:**

- Immutability
- Traceability
- Data integrity
- Secure sharing of security events

---

## Project Structure

```text
.
├── alerts
│   └── Alert data structure
│
├── analysis
│   └── Dataset analysis tools
│
├── blockchain
│   ├── api
│   │   └── Blockchain API
│   ├── chaincode
│   │   └── Hyperledger Fabric smart contract
│   └── client
│       └── Python blockchain client
│
├── classifier
│   └── Attack classification model
│
├── data
│   └── Network traffic dataset
│
├── detector
│   └── Binary anomaly detector
│
├── models
│   └── Trained machine learning models
│
├── preprocessing
│   └── Feature preparation and encoding
│
├── processed
│   └── Processed datasets
│
├── training
│   └── Model training scripts
│
├── training_multiclass
│   └── Attack classification training
│
├── tests
│   └── Unit tests
│
└── main.py
```

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd Project_IA_Blockchain_ICS_Anomaly
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install blockchain dependencies:

```bash
cd blockchain/chaincode
npm install

cd ../api
npm install
```

---

## Running the Detection System

Run:

```bash
python3 main.py
```

The system will:

1. Load the trained models
2. Read network flow data
3. Preprocess the input
4. Detect abnormal behaviour
5. Classify attacks
6. Create security alerts
7. Store malicious alerts in blockchain

---

## Hyperledger Fabric Setup

Start the Fabric network:

```bash
cd fabric-samples/test-network
./network.sh up createChannel
```

Deploy the chaincode:

```bash
alertchaincode
```

Query stored alerts:

```bash
peer chaincode query \
  -C mychannel \
  -n alertchaincode \
  -c '{"Args":["GetAllAlerts"]}'
```

---

## Technologies

| Category | Tools |
|---|---|
| **Artificial Intelligence** | Python, Scikit-learn, Pandas, Random Forest, Machine Learning classification |
| **Blockchain** | Hyperledger Fabric, Node.js, Fabric Contract API |
| **Data Processing** | Feature engineering, Data preprocessing, Encoding techniques |

---

## Future Improvements

Planned improvements:

- Real-time ICS traffic capture
- Streamlit security dashboard
- Live blockchain monitoring
- More attack categories
- Distributed IDS deployment

---

## Author

Ali Amadou
Cybersecurity Engineer
