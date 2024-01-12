import json
import os
from datetime import datetime
import base64
import boto3
s3 = boto3.client('s3')
bucket_name = os.environ['BUCKET']


def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        widget_name = event['path'][1:] if event['path'].startswith('/') else event['path']

        print(f"Event : {event}, Method : {method}, bucket: {bucket_name}")
        if method == "GET":
            if event['path'] == "/":
                body = 'No Data'
                data = s3.list_objects(Bucket=bucket_name)
                if data.get('Body', False):
                    body = {
                        'widgets': [entry['Key'] for entry in data['Body']]
                    }
                print(f"[body : {body}] [data : {data}]")
                return {
                    'statusCode': 200,
                    'headers': {},
                    'body': body
                }

            if widget_name:
                body = f'{widget_name} Not found'
                data = s3.get_object(Bucket=bucket_name, Key=widget_name)
                if data.get('Body', False):
                    body = data['Body'].read().decode('utf-8')

                return {
                    'statusCode': 200,
                    'headers': {},
                    'body': body
                }

        if method == "POST":
            if not widget_name:
                return {
                    'statusCode': 400,
                    'headers': {},
                    'body': "Widget name missing"
                }

            now = datetime.now()
            data = f"{widget_name} created: {now}"

            base64data = base64.b64encode(data.encode('utf-8'))

            s3.put_object(
                Bucket=bucket_name,
                Key=widget_name,
                Body=base64data,
                ContentType='application/json'
            )

            return {
                'statusCode': 200,
                'headers': {},
                'body': data
            }

        if method == "DELETE":
            if not widget_name:
                return {
                    'statusCode': 400,
                    'headers': {},
                    'body': "Widget name missing"
                }

            s3.delete_object(
                Bucket=bucket_name,
                Key=widget_name
            )

            return {
                'statusCode': 200,
                'headers': {},
                'body': f"Successfully deleted widget {widget_name}"
            }

        return {
            'statusCode': 400,
            'headers': {},
            'body': f"We only accept GET, POST, and DELETE, not {method}"
        }
    except Exception as error:
        body = str(error)
        return {
            'statusCode': 400,
            'headers': {},
            'body': body
        }
