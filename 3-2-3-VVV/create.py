#!/usr/bin/env python3

import boto3

dynamodb = boto3.resource("dynamodb")
table_name = "MusicTagger"
existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
client = boto3.client("dynamodb")

if table_name not in existing_tables:
    print(f"Creating table: {table_name}")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "artist", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "artist", "AttributeType": "S"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
        Tags=[{"Key": "DDBTableGroupKey-DataModeling", "Value": "DataModeling"}],
    )

    waiter = table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    response = client.describe_table(TableName=table_name)
    print(response)
