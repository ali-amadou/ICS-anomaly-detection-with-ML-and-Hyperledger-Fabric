'use strict';

const { Contract } = require('fabric-contract-api');

class AlertContract extends Contract {

    async InitLedger(ctx) {

        console.log("=== Ledger initialized ===");

    }

    async AlertExists(ctx, alertId) {

        const data = await ctx.stub.getState(alertId);

        return data && data.length > 0;

    }

    async CreateAlert(
        ctx,
        alertId,
        timestamp,
        source_ip,
        destination_ip,
        protocol,
        prediction,
        attack_type,
        severity,
        confidence,
        model
    ) {

        const exists = await this.AlertExists(ctx, alertId);

        if (exists) {

            throw new Error(`Alert ${alertId} already exists`);

        }

        const alert = {

            alertId,

            timestamp,

            source_ip,

            destination_ip,

            protocol,

            prediction,

            attack_type,

            severity,

            confidence: parseFloat(confidence),

            model

        };

        await ctx.stub.putState(

            alertId,

            Buffer.from(JSON.stringify(alert))

        );

        return JSON.stringify(alert);

    }

    async ReadAlert(ctx, alertId) {

        const data = await ctx.stub.getState(alertId);

        if (!data || data.length === 0) {

            throw new Error("Alert not found");

        }

        return data.toString();

    }

    async GetAllAlerts(ctx) {

        const iterator = await ctx.stub.getStateByRange('', '');

        const alerts = [];

        while (true) {

            const res = await iterator.next();

            if (res.value) {

                alerts.push(

                    JSON.parse(

                        res.value.value.toString()

                    )

                );

            }

            if (res.done) {

                await iterator.close();

                return JSON.stringify(alerts);

            }

        }

    }

}

module.exports = AlertContract;