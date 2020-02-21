import json

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("flights")


def lambda_handler(event, context):
    try:
        print(event)
        plane = event["queryStringParameters"]["plane"]
        result = table.query(
            IndexName="plane_iata-index",
            KeyConditionExpression=Key("plane_iata").eq(plane),
        )

        data = result["Items"]

        while "LastEvaluatedKey" in result:
            result = table.query(
                IndexName="plane_iata-index",
                KeyConditionExpression=Key("plane_iata").eq(plane),
                ExclusiveStartKey=result["LastEvaluatedKey"],
            )
            data.update(result["Items"])

        response = {
            "statusCode": 200,
            "body": json.dumps({"count": len(data), "data": data}),
            "headers": {"Content-Type": "application/json"},
        }
        return response
    except Exception as e:
        print(e)
        raise e
