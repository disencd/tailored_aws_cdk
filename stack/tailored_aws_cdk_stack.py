from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_apigateway as apigateway,
    aws_lambda as lambda_
)

from constructs import Construct


class TailoredAwsCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "WidgetStore")

        handler = lambda_.Function(self, "WidgetHandler",
                                   runtime=lambda_.Runtime.PYTHON_3_10,
                                   code=lambda_.Code.from_asset("resources"),
                                   handler="widgets.lambda_handler",
                                   environment=dict(
                                       BUCKET=bucket.bucket_name)
                                   )

        bucket.grant_read_write(handler)
        api = apigateway.RestApi(self, "widgets-api",
                                 rest_api_name="Widget Service",
                                 description="This service serves widgets.")
        get_widgets_integration = apigateway.LambdaIntegration(handler,
                                                               request_templates={
                                                                   "application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_widgets_integration)  # GET /

        widget = api.root.add_resource("{id}")

        widget_integration = apigateway.LambdaIntegration(handler)
        widget.add_method("POST", widget_integration)  # POST /{id}
        widget.add_method("GET", widget_integration)  # GET /{id}
        widget.add_method("DELETE", widget_integration)  # DELETE /{id}
