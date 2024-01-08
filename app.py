#!/usr/bin/env python3
import aws_cdk as cdk
from dynaconf import settings
from stack.tailored_aws_cdk_stack import TailoredAwsCdkStack, CDKProps


if __name__ == "__main__":
    app = cdk.App()
    TailoredAwsCdkStack(app,
                        "TailoredAwsCdkStack",
                        CDKProps(username=settings.USERNAME,
                                 password=settings.PASSWORD,
                                 group=settings.GROUP,
                                 policy=settings.POLICY),
                        env=cdk.Environment(
                            account=settings.AWS_ACCOUNT,
                            region=settings.AWS_REGION
                        )
                        )
    app.synth()
