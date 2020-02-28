import json

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("flights")


def lambda_handler(event, context):
    try:
        print(event)
        code = event["queryStringParameters"]["code"]
        result = table.query(KeyConditionExpression=Key("PK").eq(code))
        response = {
            "statusCode": 200,
            "body": json.dumps(result["Items"][0]),
            "headers": {"Content-Type": "application/json"},
        }
        return response
    except Exception as e:
        print(e)
        raise e
