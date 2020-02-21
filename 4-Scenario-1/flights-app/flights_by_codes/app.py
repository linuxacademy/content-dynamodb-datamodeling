import json

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("flights")


def lambda_handler(event, context):
    try:
        print(event)
        src = event["queryStringParameters"]["src"]
        dst = event["queryStringParameters"]["dst"]
        result = (
            table.query(KeyConditionExpression=Key("PK").eq(src) & Key("SK").eq(dst)),
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(result["Items"][0]),
            "headers": {"Content-Type": "application/json"},
        }
        return response
    except Exception as e:
        print(e)
        raise e
