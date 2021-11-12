from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam,
    aws_ec2 as ec2,
)

from cdk_dynamo_table_view import TableViewer
from .hitcounter import HitCounter

class CdkWorkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler',)
            
            
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
            
        )
            
        apigw.LambdaRestApi(
            self, 'End  point',
            #handler = my_lambda,
            handler = hello_with_counter._handler,    
        )
        TableViewer(
            self, 'ViewHitCounter',
            title = 'HIT COUNTER NI AJ',
            table = hello_with_counter.table ,
            
            
        )
        
        
        
        
class Ec2SampleStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)  
        
        
        vpc = ec2.Vpc(self, "VPC",
            cidr='10.107.0.0/24', #CIDR entry, can use 10.x.x.x. Decided to use this value as it's the minimum for 2 availability zones
            nat_gateways=0,
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="public",subnet_type=ec2.SubnetType.PUBLIC)                
            ]
           
        )
        
        
        
         # Create first the subnet
        publicSecurityGroup = ec2.SecurityGroup(self, "PublicSecurityGroup",
            vpc=vpc,
            allow_all_outbound=True,
        )
        
        # This is the default when creating an EC2 instance from the console
        # Bad security practice though. For now, we use this.
        publicSecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            'Allows SSH access from Internet'
        )
         
         
        # Adds entry to security group to make it pingable from the internet
        #https://stackoverflow.com/questions/21981796/cannot-ping-aws-ec2-instance
        #https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Port.html
        publicSecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.icmp_ping(),
            'Allows EC2 to be pingable from the Internet'
        )   
        
        
        # AMI
        # Gets the latest AMI id
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2, # OS is Amazon Linux 2
            edition=ec2.AmazonLinuxEdition.STANDARD,             # Default
            virtualization=ec2.AmazonLinuxVirt.HVM,              # Default
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE       # General Purpose Storage. We can use Provsioned or Magnetic
        )

        instance = ec2.Instance(self, "Instance",
            instance_type=ec2.InstanceType("t3.nano"),
            machine_image=amzn_linux,
            vpc = vpc,
            security_group=publicSecurityGroup,
            instance_name="AJ_EC2", 
            key_name="AJ_Keypair"        # NOTE: This needs to be created first in AWS Console. Check EC2 -> Network & Security -> Key Pair
        )