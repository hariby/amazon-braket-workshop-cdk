import json
import pytest

from aws_cdk import core
from braket-workshop-cdk.braket_workshop_cdk_stack import BraketWorkshopCdkStack


def get_template():
    app = core.App()
    BraketWorkshopCdkStack(app, "braket-workshop-cdk")
    return json.dumps(app.synth().get_stack("braket-workshop-cdk").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
