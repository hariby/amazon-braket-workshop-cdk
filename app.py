#!/usr/bin/env python3

from aws_cdk import core

from braket_workshop_cdk.braket_workshop_cdk_stack import BraketWorkshopIAMStack


app = core.App()
BraketWorkshopIAMStack(app, "braket-workshop-cdk", env={'region': 'us-west-2'})

app.synth()
