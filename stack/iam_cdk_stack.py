from aws_cdk import (
    Stack, Tags
)
from dataclasses import dataclass
import aws_cdk.aws_iam as iam
from aws_cdk.aws_s3_assets import Asset
import aws_cdk.aws_ec2 as ec2
from constructs import Construct
import os


@dataclass
class CDKProps:
    """
    Stack Props
    """
    user: str
    role: str
    vpc: str
    policy: str
    s3_bucket: str


class IamCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_props: CDKProps, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Tags.of(scope).add("cdk", "IamCdkStack")

        user = iam.User(self, cdk_props.user)

        user_s3_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["S3:*"],
            resources=["*"]
        )

        policy = iam.Policy(self, f"{cdk_props.user}-policy",
                            statements=[user_s3_policy])

        user.attach_inline_policy(policy)

        role = iam.Role(self, f"{cdk_props.user}-EC2-Role",
                        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

        role.attach_inline_policy(policy)

        vpc = ec2.Vpc(self, cdk_props.vpc,
                      nat_gateways=0,
                      subnet_configuration=[ec2.SubnetConfiguration(name="public", subnet_type=ec2.SubnetType.PUBLIC)]
                      )

        sg = ec2.SecurityGroup(self,
                               id=f"{cdk_props.vpc}-SG",
                               vpc=vpc,
                               description='Allow SSH access to EC2 Instances',
                               allow_all_outbound=True)

        sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), 'Welcome to whole ssh users in this world')

        # AMI
        amzn_linux = ec2.MachineImage.latest_amazon_linux(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            virtualization=ec2.AmazonLinuxVirt.HVM,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )

        # Instance
        instance = ec2.Instance(self, "Instance",
                                instance_type=ec2.InstanceType("t3.nano"),
                                machine_image=amzn_linux,
                                vpc=vpc,
                                role=role,
                                security_group=sg
                                )

        # Script in S3 as Asset
        _dirname = os.path.dirname(__file__)

        asset = Asset(self, "Asset", path=os.path.join(_dirname, "../ec2-configure.sh"))
        local_path = instance.user_data.add_s3_download_command(
            bucket=asset.bucket,
            bucket_key=asset.s3_object_key
        )

        # Userdata executes script from S3
        instance.user_data.add_execute_file_command(
            file_path=local_path
        )
        asset.grant_read(instance.role)
