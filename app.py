#!/usr/bin/env python3

from aws_cdk import core

from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack
#from cdk_workshop.cdk_workshop_stack import Ec2SampleStack


app = core.App()

CdkWorkshopStack(app, "cdk-workshop")
#Ec2SampleStack(app, "EC2-workshop")


app.synth()
