#!/usr/bin/env python3

from aws_cdk import core

from braket_workshop_cdk.braket_workshop_cdk_stack import BraketWorkshopIAMStack, BraketWorkshopNotebookStack


app = core.App()
iam_stack = BraketWorkshopIAMStack(app, "braket-workshop-iam", env={'region': 'us-west-2'})

notebook_role_arn = iam_stack.braket_notebook_role.role_arn

BraketWorkshopNotebookStack(app, "braket-workshop-notebook-us-east-1", notebook_role_arn=notebook_role_arn, partition_remainder=0, env={'region': 'us-east-1'})
BraketWorkshopNotebookStack(app, "braket-workshop-notebook-us-west-1", notebook_role_arn=notebook_role_arn, partition_remainder=1, env={'region': 'us-west-1'})
BraketWorkshopNotebookStack(app, "braket-workshop-notebook-us-west-2", notebook_role_arn=notebook_role_arn, partition_remainder=2, env={'region': 'us-west-2'})

app.synth()
