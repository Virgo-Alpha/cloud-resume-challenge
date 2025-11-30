import json
import os
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ["TABLE_NAME"]
PRIMARY_KEY = os.environ.get("PRIMARY_KEY", "pk")
COUNTER_ATTR = os.environ.get("COUNTER_ATTR", "visitCount")
AWS_REGION = os.environ.get("AWS_REGION", "eu-west-1")  # your region

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)
cloudwatch = boto3.client("cloudwatch", region_name=AWS_REGION)


def lambda_handler(event, context):
    try:
        resp = table.update_item(
            Key={PRIMARY_KEY: "visitors"},
            UpdateExpression=f"SET {COUNTER_ATTR} = if_not_exists({COUNTER_ATTR}, :start) + :inc",
            ExpressionAttributeValues={
                ":start": 0,
                ":inc": 1,
            },
            ReturnValues="UPDATED_NEW",
        )
        new_count = int(resp["Attributes"][COUNTER_ATTR])

        # 🔹 Emit a custom metric for page views
        cloudwatch.put_metric_data(
            Namespace="CloudResume",
            MetricData=[
                {
                    "MetricName": "PageView",
                    "Value": 1,
                    "Unit": "Count",
                }
            ],
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"count": new_count}),
        }

    except ClientError as e:
        print(f"Error updating visitor count: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"}),
        }
