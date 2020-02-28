#!/usr/bin/env python3

import boto3

dynamodb = boto3.resource("dynamodb")
client = dynamodb.meta.client
table_name = "employees"
existing_tables = client.list_tables()["TableNames"]

if table_name not in existing_tables:
    print(f"Creating table {table_name}. This can take some time to complete.")
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "emp_no", "KeyType": "HASH"},
            {"AttributeName": "salary", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "emp_no", "AttributeType": "N"},
            {"AttributeName": "salary", "AttributeType": "N"},
            {"AttributeName": "department_name", "AttributeType": "S"},
            {"AttributeName": "title", "AttributeType": "S"},
            {"AttributeName": "last_name", "AttributeType": "S"},
            {"AttributeName": "salary_to_date", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "department_name-index",
                "KeySchema": [{"AttributeName": "department_name", "KeyType": "HASH"},],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "department_manager-index",
                "KeySchema": [
                    {"AttributeName": "department_name", "KeyType": "HASH"},
                    {"AttributeName": "manager_name", "KeyType": "RANGE"},
                ],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "title-index",
                "KeySchema": [{"AttributeName": "title", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "last_name-index",
                "KeySchema": [{"AttributeName": "last_name", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
            {
                "IndexName": "salary-index",
                "KeySchema": [
                    {"AttributeName": "salary_to_date", "KeyType": "HASH"},
                    {"AttributeName": "salary", "KeyType": "RANGE"},
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
