#!/usr/bin/env python3

import boto3

dynamodb = boto3.resource("dynamodb")
client = dynamodb.meta.client
existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
table_name = "Versioning"

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "Version", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "ID", "AttributeType": "N"},
            {"AttributeName": "Version", "AttributeType": "N"},
        ],
        BillingMode="PAY_PER_REQUEST",
        Tags=[{"Key": "DDBTableGroupKey-DataModeling", "Value": "DataModeling"}],
    )

    waiter = client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    table = dynamodb.Table(table_name)
