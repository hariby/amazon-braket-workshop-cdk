import json
import pytest

from aws_cdk import core
from braket_workshop_cdk.braket_workshop_cdk_stack import BraketWorkshopIAMStack


def get_template():
    app = core.App()
    BraketWorkshopIAMStack(app, "braket-workshop-cdk")
    return json.dumps(app.synth().get_stack("braket-workshop-cdk").template)


def test_iam_group_created():
    assert("AWS::IAM::Group" in get_template())


def test_iam_user_created():
    assert("AWS::IAM::User" in get_template())


def test_iam_user_secret():
    assert("AWS::SecretsManager::Secret" in get_template())


def test_iam_role_created():
    assert("AWS::IAM::Role" in get_template())
