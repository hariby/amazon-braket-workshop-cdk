#!/usr/bin/env python3

from aws_cdk import core

from braket_workshop_cdk.braket_workshop_cdk_stack import BraketWorkshopCdkStack


app = core.App()
BraketWorkshopCdkStack(app, "braket-workshop-cdk", env={'region': 'us-west-2'})

app.synth()
