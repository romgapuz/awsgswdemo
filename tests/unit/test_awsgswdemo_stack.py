import json
import pytest

from aws_cdk import core
from awsgswdemo.awsgswdemo_stack import AwsgswdemoStack


def get_template():
    app = core.App()
    AwsgswdemoStack(app, "awsgswdemo")
    return json.dumps(app.synth().get_stack("awsgswdemo").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
