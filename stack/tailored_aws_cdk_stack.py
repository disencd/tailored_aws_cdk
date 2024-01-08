from aws_cdk import (
    Stack, SecretValue
)
from dataclasses import dataclass
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam
from constructs import Construct


@dataclass
class CDKProps:
    """
    Stack Props
    """
    username: str
    group: str
    policy: str
    password: str


class TailoredAwsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, cdk_props: CDKProps, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user = iam.User(self, cdk_props.username, password=SecretValue.plain_text(cdk_props.password))
        group = iam.Group(self, cdk_props.group)

        policy = iam.Policy(self, cdk_props.policy)
        policy.attach_to_user(user)
        group.attach_inline_policy(policy)
        group.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
