#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
client = dynamodb.meta.client
table_name = "Projects"
gsi_name = "Item-index"
existing_tables = client.list_tables()["TableNames"]

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "ID", "KeyType": "HASH"},
            {"AttributeName": "Item", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "ID", "AttributeType": "S"},
            {"AttributeName": "Item", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    waiter = client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    table = dynamodb.Table(table_name)

# Create Global Secondary Index

try:
    print(f"Creating GSI {gsi_name}")
    resp = client.update_table(
        TableName=table_name,
        AttributeDefinitions=[{"AttributeName": "Item", "AttributeType": "S"}],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": gsi_name,
                    "KeySchema": [{"AttributeName": "Item", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                }
            }
        ],
    )
    print(f"GSI {gsi_name} added. This can take some time to complete.")
except Exception as e:
    print("Error updating table:")
    print(e)

# Populate some data

try:
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                "ID": "PROJECT1",
                "Item": "PROJECT1",
                "name": "Blue Book",
                "date_started": "2019-11-10",
                "active": "Y",
            }
        ),
        batch.put_item(
            Item={
                "ID": "PROJECT1",
                "Item": "EMPLOYEE1",
                "date_joined": "2020-02-06",
                "active": "Y",
            }
        ),
        batch.put_item(
            Item={
                "ID": "PROJECT1",
                "Item": "EMPLOYEE2",
                "date_joined": "2019-11-11",
                "active": "N",
            }
        ),
        batch.put_item(
            Item={
                "ID": "EMPLOYEE1",
                "Item": "EMPLOYEE1",
                "first_name": "Mike",
                "last_name": "Portnoy",
                "email": "mp@example.com",
            }
        ),
        batch.put_item(
            Item={
                "ID": "EMPLOYEE2",
                "Item": "EMPLOYEE2",
                "first_name": "Jim",
                "last_name": "Matheos",
                "email": "jm@example.com",
            }
        ),


except ClientError as e:
    print(e)
