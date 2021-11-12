import json
import pytest

from aws_cdk import (
    core, 
    aws_lambda as _lambda, 
    assertions,
)
from cdk_workshop.hitcounter import HitCounter
from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack



def get_template():
    app = core.App()
    CdkWorkshopStack(app, "cdk-workshop")
    return json.dumps(app.synth().get_stack("cdk-workshop").template)


#def test_sqs_queue_created():
#    assert("AWS::SQS::Queue" in get_template())


#def test_sns_topic_created():
#    assert("AWS::SNS::Topic" in get_template())

def test_dynamodb_table_created():
    stack = core.Stack()
    HitCounter(stack, "HitCounter",
            downstream=_lambda.Function(stack, "TestFunction",
                runtime=_lambda.Runtime.NODEJS_14_X,
                handler='hello.handler',
                code=_lambda.Code.from_asset('lambda')),
    )
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 1)