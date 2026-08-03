import subprocess
import uuid


class BlockchainClient:

    def submit_alert(self, alert):

        alert_id = str(uuid.uuid4())

        cmd = f"""
peer chaincode invoke \
-o localhost:7050 \
--ordererTLSHostnameOverride orderer.example.com \
--tls \
--cafile "$HOME/fabric-samples/test-network/organizations/ordererOrganizations/example.com/tlsca/tlsca.example.com-cert.pem" \
-C mychannel \
-n alertchaincode \
--peerAddresses localhost:7051 \
--tlsRootCertFiles "$HOME/fabric-samples/test-network/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" \
--peerAddresses localhost:9051 \
--tlsRootCertFiles "$HOME/fabric-samples/test-network/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" \
--waitForEvent \
-c '{{"Args":[
"CreateAlert",
"{alert_id}",
"{alert.timestamp}",
"{alert.source_ip}",
"{alert.destination_ip}",
"{alert.protocol}",
"{alert.prediction}",
"{alert.attack_type}",
"{alert.severity}",
"{alert.confidence}",
"{alert.model}"
]}}'
"""

        result = subprocess.run(
            ["bash", "-c", cmd],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        print(result.stdout)

        return alert_id