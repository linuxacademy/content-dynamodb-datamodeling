#!/usr/bin/env python3

import boto3

dynamodb = boto3.resource("dynamodb")
client = boto3.client("dynamodb")
table_name = "flights"

existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "PK", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "PK", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "src_ap", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "src_ap-index",
                "KeySchema": [{"AttributeName": "src_ap", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "KEYS_ONLY"},
            }
        ],
        BillingMode="PAY_PER_REQUEST",
        Tags=[{"Key": "DDBTableGroupKey-DataModeling", "Value": "DataModeling"}],
    )

    dynamodb.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    table = dynamodb.Table(table_name)
