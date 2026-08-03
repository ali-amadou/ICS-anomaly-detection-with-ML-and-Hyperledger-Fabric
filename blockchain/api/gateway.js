'use strict';

const path = require('path');
const fs = require('fs');

const {
    Gateway,
    Wallets
} = require('fabric-network');

const crypto = require('crypto');

const channelName = 'mychannel';
const chaincodeName = 'alertchaincode';

const basePath =
    path.join(
        process.env.HOME,
        'fabric-samples',
        'test-network',
        'organizations',
        'peerOrganizations',
        'org1.example.com'
    );

const ccpPath =
    path.join(
        basePath,
        'connection-org1.json'
    );

const walletPath =
    path.join(__dirname, 'wallet');

let contract = null;
let gateway = null;

async function connect() {

    if (contract) {
        return contract;
    }

    const ccp = JSON.parse(
        fs.readFileSync(ccpPath, 'utf8')
    );

    const wallet =
        await Wallets.newFileSystemWallet(walletPath);

    const identity =
        await wallet.get('appUser');

    if (!identity) {

        throw new Error(
            'Identity appUser not found in wallet.'
        );

    }

    gateway = new Gateway();

    await gateway.connect(
        ccp,
        {
            wallet,
            identity: 'appUser',
            discovery: {
                enabled: true,
                asLocalhost: true
            }
        }
    );

    const network =
        await gateway.getNetwork(channelName);

    contract =
        network.getContract(chaincodeName);

    console.log(
        'Gateway connected successfully.'
    );

    return contract;

}

async function createAlert(alert) {

    const contract =
        await connect();

    const alertId =
        "ALERT-" +
        crypto.randomUUID();

    await contract.submitTransaction(

        "CreateAlert",

        alertId,

        alert.timestamp,

        alert.source_ip,

        alert.destination_ip,

        alert.protocol,

        alert.prediction,

        alert.attack_type,

        alert.severity,

        alert.confidence.toString(),

        alert.model

    );

    return {

        success: true,

        alertId

    };

}

async function readAlert(id) {

    const contract =
        await connect();

    const result =
        await contract.evaluateTransaction(

            "ReadAlert",

            id

        );

    return JSON.parse(

        result.toString()

    );

}

async function getAllAlerts() {

    const contract =
        await connect();

    const result =
        await contract.evaluateTransaction(

            "GetAllAlerts"

        );

    return JSON.parse(

        result.toString()

    );

}

module.exports = {

    createAlert,

    readAlert,

    getAllAlerts

};