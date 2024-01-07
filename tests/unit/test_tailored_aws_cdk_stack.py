import aws_cdk as core
import aws_cdk.assertions as assertions

from tailored_aws_cdk.tailored_aws_cdk_stack import TailoredAwsCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in tailored_aws_cdk/tailored_aws_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = TailoredAwsCdkStack(app, "tailored-aws-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
