import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from detector.binary_detector import BinaryDetector
from blockchain.client.blockchain_client import BlockchainClient

# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="ICS Network Anomaly Detection Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ ICS Network Anomaly Detection Dashboard")
st.caption("Machine Learning + Hyperledger Fabric")

DATASET = BASE_DIR / "data" / "output_bottom.csv"

MAX_BLOCKCHAIN_ALERTS = 10

# -------------------------------------------------------
# Dataset
# -------------------------------------------------------

@st.cache_data
def load_dataset():
    return pd.read_csv(DATASET)

df = load_dataset()

st.subheader("Detection settings")

max_flows = st.selectbox(
    "Number of flows to analyse",
    [100, 500, 1000, 2000, len(df)],
    index=3,
    format_func=lambda x: "Entire dataset" if x == len(df) else str(x)
)

df_analysis = df.head(max_flows)

total = len(df_analysis)
# -------------------------------------------------------
# Initial KPIs
# -------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Flows Analysed", total)
c2.metric("Detected Attacks", "-")
c3.metric("Normal Traffic", "-")
c4.metric("Stored in Blockchain", "-")

st.divider()

st.info(
    f"""
Dataset loaded successfully.

Dataset contains {len(df)} flows.\n\n

The dashboard will analyse the first {len(df_analysis)} flows.

Flows available : **{len(df)}**

Click **Run Detection** to analyse the complete dataset.
"""
)



# -------------------------------------------------------
# Detection
# -------------------------------------------------------

if st.button("🚀 Run Detection", use_container_width=True):

    detector = BinaryDetector()
    client = BlockchainClient()

    detected_alerts = []

    saved = 0

    progress = st.progress(0)

    status = st.empty()

    total = len(df_analysis)

    for i, (_, row) in enumerate(df_analysis.iterrows()):

        status.text(f"Analysing flow {i+1}/{total}")

        flow = row.to_dict()

        alert = detector.predict(flow)

        if alert.prediction == "Attack":

            detected_alerts.append(alert.to_dict())

            if saved < MAX_BLOCKCHAIN_ALERTS:

                client.submit_alert(alert)
                saved += 1

        progress.progress((i + 1) / total)

    progress.empty()
    status.empty()

    attacks = len(detected_alerts)
    normal = total - attacks

    st.success(
        f"""
Detection completed successfully.

• Total flows analysed : {total}

• Attacks detected : {attacks}

• Alerts stored in Hyperledger Fabric : {saved}
"""
    )

    st.divider()

    # ---------------------------------------------------
    # Final KPIs
    # ---------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Flows", total)

    c2.metric("Detected Attacks", attacks)

    c3.metric("Normal Traffic", normal)

    c4.metric("Stored in Blockchain", saved)

    st.divider()

    # ---------------------------------------------------
    # Prediction statistics
    # ---------------------------------------------------

    prediction_stats = pd.DataFrame(
        {
            "Prediction": ["Attack", "Normal"],
            "Count": [attacks, normal]
        }
    )

    st.subheader("📊 Prediction Distribution")

    st.bar_chart(
        prediction_stats.set_index("Prediction")
    )

    # ---------------------------------------------------
    # Severity statistics
    # ---------------------------------------------------

    if attacks > 0:

        severity_df = pd.DataFrame(detected_alerts)

        severity_count = (
            severity_df["severity"]
            .value_counts()
            .sort_index()
        )

        st.subheader("📊 Severity Distribution")

        st.bar_chart(severity_count)

    # ---------------------------------------------------
    # Detected attacks
    # ---------------------------------------------------

    st.divider()

    st.subheader("🚨 Detected Attacks")

    if attacks == 0:

        st.info("No attack detected.")

    else:

        alerts_df = pd.DataFrame(detected_alerts)

        st.dataframe(
            alerts_df,
            use_container_width=True,
            hide_index=True
        )

    # ---------------------------------------------------
    # Hyperledger Fabric
    # ---------------------------------------------------

    st.divider()

    st.subheader("⛓️ Alerts Stored in Hyperledger Fabric")

    try:

        fabric_alerts = client.get_all_alerts()

        if len(fabric_alerts) == 0:

            st.info("Blockchain ledger is empty.")

        else:

            fabric_df = pd.DataFrame(fabric_alerts)

            st.dataframe(
                fabric_df,
                use_container_width=True,
                hide_index=True
            )

            st.success("🟢 Connected to Hyperledger Fabric")

    except Exception as e:

        st.error("🔴 Unable to read the blockchain.")

        st.exception(e)