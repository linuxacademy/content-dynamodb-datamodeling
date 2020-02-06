#!/usr/bin/env python3

import hashlib
import os

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

# boto3.set_stream_logger(name="botocore")  # uncomment to enable debug logging
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Versioning")
client = boto3.client("dynamodb")


def get_current():
    """Get current version (always v0)"""
    response = table.query(
        KeyConditionExpression=Key("ID").eq(1) & Key("Version").eq(0)
    )
    return response["Items"][0]["CurrentVersion"]


try:

    # --BEGIN-- Comment this out if running subsequent times

    print("Writing first version - both v0 and v1 simultaneously")

    table.put_item(Item={"ID": 1, "Version": 0, "CurrentVersion": 1})
    table.put_item(
        Item={
            "ID": 1,
            "Version": 1,
            "CommitID": hashlib.sha1(os.urandom(32)).hexdigest(),
        },
    )

    # --END-- Comment this out if running subsequent times

    current = get_current()

    print(f"CurrentVersion = {current}")

    current += 1

    print(f"Writing new version {current} and updating v0 to point to v{current}")

    response = client.transact_write_items(
        TransactItems=[
            {
                "Update": {
                    "TableName": table.name,
                    "Key": {"ID": {"N": "1"}, "Version": {"N": "0"}},
                    "UpdateExpression": "set CurrentVersion = :cv",
                    "ExpressionAttributeValues": {":cv": {"N": str(current)}},
                    "ConditionExpression": "CurrentVersion <> :cv",
                },
            },
            {
                "Put": {
                    "TableName": table.name,
                    "Item": {
                        "ID": {"N": "1"},
                        "Version": {"N": str(current)},
                        "CommitID": {"S": hashlib.sha1(os.urandom(32)).hexdigest()},
                    },
                    "ConditionExpression": "attribute_not_exists(ID) AND attribute_not_exists(Version)",
                },
            },
        ]
    )

    current = get_current()
    print(f"Current version: {current}")

except client.exceptions.TransactionCanceledException as tce:
    print(tce)
except ClientError as ce:
    print(ce)
