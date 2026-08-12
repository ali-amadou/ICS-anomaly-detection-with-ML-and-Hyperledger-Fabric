#!/bin/bash

echo "========================================"
echo " ICS Anomaly Detection Demo"
echo "========================================"

# ---------------------------------------
# Start Hyperledger Fabric
# ---------------------------------------

cd ~/fabric-samples/test-network
./network.sh up

# ---------------------------------------
# Start Gateway API
# ---------------------------------------

if ! pgrep -f "node server.js" > /dev/null; then
    echo "Starting Gateway..."
    cd /mnt/f/Project_IA_Blockchain_ICS_Anomaly/blockchain/api
    nohup node server.js > gateway.log 2>&1 &
else
    echo "Gateway already running."
fi

# ---------------------------------------
# Start Streamlit
# ---------------------------------------

if ! pgrep -f "streamlit run dashboard/app.py" > /dev/null; then
    echo "Starting Streamlit..."
    cd /mnt/f/Project_IA_Blockchain_ICS_Anomaly
    nohup streamlit run dashboard/app.py > streamlit.log 2>&1 &
else
    echo "Streamlit already running."
fi

echo "Waiting for Streamlit..."

until nc -z localhost 8501
do
    sleep 1
done

echo "Opening Dashboard..."

cmd.exe /c start http://localhost:8501

echo ""
echo "========================================"
echo "Demo ready!"
echo "========================================"