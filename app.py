#!/usr/bin/env python3

from aws_cdk import core
from awsgswdemo.awsgswdemo_stack import AwsgswdemoStack

env = {'region': 'us-west-2'}

app = core.App()
AwsgswdemoStack(app, "awsgswdemo", env=env)

app.synth()
