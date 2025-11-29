import os
import json

import boto3
from moto import mock_aws


TABLE_NAME = "test-VisitorCount"


@mock_aws
def test_lambda_increments_counter():
    # Arrange: create mock table
    os.environ["TABLE_NAME"] = TABLE_NAME
    os.environ["PRIMARY_KEY"] = "pk"
    os.environ["COUNTER_ATTR"] = "visitCount"
    os.environ["AWS_REGION"] = "us-east-1"

    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName=TABLE_NAME,
        BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[{"AttributeName": "pk", "AttributeType": "S"}],
        KeySchema=[{"AttributeName": "pk", "KeyType": "HASH"}],
    )

    # Import here so table/env are set up before app module loads
    from backend.src import app

    # Act: call twice
    first = app.lambda_handler({}, None)
    second = app.lambda_handler({}, None)

    # Assert
    assert first["statusCode"] == 200
    assert second["statusCode"] == 200

    body1 = json.loads(first["body"])
    body2 = json.loads(second["body"])

    assert body1["count"] == 1
    assert body2["count"] == 2
