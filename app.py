#!/usr/bin/env python3
import aws_cdk as cdk
from dynaconf import settings
from stack.iam_cdk_stack import IamCdkStack, CDKProps

# from stack.tailored_aws_cdk_stack import TailoredAwsCdkStack

if __name__ == "__main__":
    app = cdk.App()

    IamCdkStack(app,
                "IamCdkStack",
                CDKProps(user=settings.USER,
                         role=settings.ROLE,
                         vpc=settings.VPC,
                         policy=settings.POLICY,
                         s3_bucket=settings.S3_BUCKET),
                env=cdk.Environment(
                    account=settings.AWS_ACCOUNT,
                    region=settings.AWS_REGION
                )
            )

    # Creating a serverless application using the AWS CDK
    # https://docs.aws.amazon.com/cdk/v2/guide/serverless_example.html
    # TailoredAwsCdkStack(app,
    #                     "TailoredAwsCdkStack",
    #                     CDKProps(role=settings.ROLE,
    #                              policy=settings.POLICY,
    #                              s3_bucket=settings.S3_BUCKET),
    #                     env=cdk.Environment(
    #                         account=settings.AWS_ACCOUNT,
    #                         region=settings.AWS_REGION
    #                     )
    #                     )

    # TailoredECSCdkStack(app,
    #                     "TailoredECSCdkStack",
    #                     EcsCDKProps(role=settings.ROLE,
    #                              policy=settings.POLICY,
    #                              s3_bucket=settings.S3_BUCKET),
    #                     env=cdk.Environment(
    #                         account=settings.AWS_ACCOUNT,
    #                         region=settings.AWS_REGION
    #                     )
    #                     )
    app.synth()
