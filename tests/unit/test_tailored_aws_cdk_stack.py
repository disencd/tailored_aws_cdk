import aws_cdk as core
import aws_cdk.assertions as assertions
from dynaconf import Dynaconf
from stack.tailored_aws_cdk_stack import TailoredAwsCdkStack, CDKProps

settings = Dynaconf(
    settings_file=["settings.toml"]
)

# example tests. To run these tests, uncomment this file along with the example
# resource in stack/tailored_aws_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TailoredAwsCdkStack(app, "tailored-aws-cdk",
                                CDKProps(username=settings.USERNAME,
                                 password=settings.PASSWORD,
                                 group=settings.GROUP,
                                 policy=settings.POLICY),
                        env=core.Environment(
                            account=settings.AWS_ACCOUNT,
                            region=settings.AWS_REGION
                        ))
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
