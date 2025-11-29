import json
import os
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ["TABLE_NAME"]
PRIMARY_KEY = os.environ.get("PRIMARY_KEY", "pk")
COUNTER_ATTR = os.environ.get("COUNTER_ATTR", "visitCount")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Simple visitor counter Lambda.
    Each invocation:
      - upserts a single item with pk='visitors'
      - increments visitCount atomically
      - returns the new count as JSON
    """

    try:
        resp = table.update_item(
            Key={PRIMARY_KEY: "visitors"},
            # if_not_exists allows first-time creation
            UpdateExpression=f"SET {COUNTER_ATTR} = if_not_exists({COUNTER_ATTR}, :start) + :inc",
            ExpressionAttributeValues={
                ":start": 0,
                ":inc": 1,
            },
            ReturnValues="UPDATED_NEW",
        )
        new_count = int(resp["Attributes"][COUNTER_ATTR])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"count": new_count}),
        }

    except ClientError as e:
        # Log the error for CloudWatch; return generic 500 to client
        print(f"Error updating visitor count: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal server error"}),
        }
