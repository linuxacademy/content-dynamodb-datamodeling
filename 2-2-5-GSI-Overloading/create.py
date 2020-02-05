#!/usr/bin/env python3

import boto3

dynamodb = boto3.resource("dynamodb")
client = dynamodb.meta.client
table_name = "Inventory"
existing_tables = client.list_tables()["TableNames"]

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "ID", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
            {"AttributeName": "Data", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "Data-index",
                "KeySchema": [
                    {"AttributeName": "SK", "KeyType": "HASH"},
                    {"AttributeName": "Data", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode="PAY_PER_REQUEST",
        Tags=[{"Key": "DDBTableGroupKey-DataModeling", "Value": "DataModeling"}],
    )

    waiter = client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    table = dynamodb.Table(table_name)
