import json
import subprocess
import uuid


class BlockchainClient:

    def _fabric_env(self):

        return """
cd ~/fabric-samples/test-network

export PATH=$HOME/fabric-samples/bin:/usr/local/bin:/usr/bin:/bin
export FABRIC_CFG_PATH=$HOME/fabric-samples/config

export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID=Org1MSP
export CORE_PEER_MSPCONFIGPATH=$HOME/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_TLS_ROOTCERT_FILE=$HOME/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_ADDRESS=localhost:7051
"""

    def submit_alert(self, alert):

        alert_id = str(uuid.uuid4())

        payload = {
            "Args": [
                "CreateAlert",
                alert_id,
                alert.timestamp,
                alert.source_ip,
                alert.destination_ip,
                alert.protocol,
                alert.prediction,
                alert.attack_type,
                alert.severity,
                str(alert.confidence),
                alert.model,
            ]
        }

        command = (
            self._fabric_env()
            + f"""

peer chaincode invoke \
-o localhost:7050 \
--ordererTLSHostnameOverride orderer.example.com \
--tls \
--cafile $HOME/fabric-samples/test-network/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem \
-C mychannel \
-n alertchaincode \
--peerAddresses localhost:7051 \
--tlsRootCertFiles $HOME/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt \
--peerAddresses localhost:9051 \
--tlsRootCertFiles $HOME/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt \
--waitForEvent \
-c '{json.dumps(payload)}'
"""
        )

        result = subprocess.run(
            ["wsl", "bash", "-c", command],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return alert_id

    def get_all_alerts(self):

        payload = {
            "Args": [
                "GetAllAlerts"
            ]
        }

        command = (
            self._fabric_env()
            + f"""

peer chaincode query \
-C mychannel \
-n alertchaincode \
-c '{json.dumps(payload)}'
"""
        )

        result = subprocess.run(
            ["wsl", "bash", "-c", command],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        output = result.stdout.strip()

        if output == "":
            return []

        return json.loads(output)