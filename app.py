#!/usr/bin/env python3
import aws_cdk as cdk
from dynaconf import settings
from stack.tailored_aws_cdk_stack import TailoredAwsCdkStack, CDKProps

if __name__ == "__main__":
    app = cdk.App()
    TailoredAwsCdkStack(app,
                        "TailoredAwsCdkStack",
                        CDKProps(role=settings.ROLE,
                                 policy=settings.POLICY,
                                 s3_bucket=settings.S3_BUCKET),
                        env=cdk.Environment(
                            account=settings.AWS_ACCOUNT,
                            region=settings.AWS_REGION
                        )
                        )
    app.synth()
