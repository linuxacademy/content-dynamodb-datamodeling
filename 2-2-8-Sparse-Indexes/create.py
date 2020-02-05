#!/usr/bin/env python3

import random

import boto3

dynamodb = boto3.resource("dynamodb")
client = dynamodb.meta.client
table_name = "Orders-SparseIndex"
existing_tables = client.list_tables()["TableNames"]

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "CustomerID", "KeyType": "HASH"},
            {"AttributeName": "OrderID", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "CustomerID", "AttributeType": "S"},
            {"AttributeName": "OrderID", "AttributeType": "S"},
            {"AttributeName": "IsOpen", "AttributeType": "N"},
        ],
        LocalSecondaryIndexes=[
            {
                "IndexName": "IsOpen-index",
                "KeySchema": [
                    {"AttributeName": "CustomerID", "KeyType": "HASH"},
                    {"AttributeName": "IsOpen", "KeyType": "RANGE"},
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

count = 0
for _ in range(1, 50):
    item = {}
    item["CustomerID"] = str(random.randint(100000, 900000))
    for _ in range(1, 10):
        item["OrderID"] = str(random.randint(1000000, 9000000))
        is_open = random.choice([1] * 2 + [0] * 8)  # 20% open orders
        if is_open == 1:
            item["IsOpen"] = 1  # don't write closed orders
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
            count += 1
            if count % 100 == 0:
                print(f"{count} items written...")
