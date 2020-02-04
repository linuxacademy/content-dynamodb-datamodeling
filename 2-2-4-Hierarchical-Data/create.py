#!/usr/bin/env python3

import boto3

client = boto3.client("dynamodb")
table_name = "TargetStores"
existing_tables = client.list_tables()["TableNames"]

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")

try:
    resp = client.create_table(
        AttributeDefinitions=[
            {"AttributeName": "State", "AttributeType": "S"},
            {"AttributeName": "StateCityPostalcode", "AttributeType": "S"},
            {"AttributeName": "StoreNumber", "AttributeType": "S"},
        ],
        TableName=table_name,
        KeySchema=[{"AttributeName": "StoreNumber", "KeyType": "HASH"}],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "Location-index",
                "KeySchema": [
                    {"AttributeName": "State", "KeyType": "HASH"},
                    {"AttributeName": "StateCityPostalcode", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
        BillingMode="PAY_PER_REQUEST",
    )
    print("Table created successfully!")
except Exception as e:
    print("Error creating table:")
    print(e)
