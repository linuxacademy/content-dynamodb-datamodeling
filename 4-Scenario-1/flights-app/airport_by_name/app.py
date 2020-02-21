import json

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("flights")


def lambda_handler(event, context):
    try:
        print(event)
        result = table.query(
            IndexName="src_ap-index",
            KeyConditionExpression=Key("src_ap").eq(
                event["queryStringParameters"]["name"]
            ),
            Limit=1,
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(result["Items"][0]["PK"]),
            "headers": {"Content-Type": "application/json"},
        }
        return response
    except Exception as e:
        print(e)
        raise e
