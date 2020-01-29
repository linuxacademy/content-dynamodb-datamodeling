#!/usr/bin/env python3

from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table_name = "Orders"
existing_tables = dynamodb.meta.client.list_tables()["TableNames"]

if table_name not in existing_tables:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "OrderID", "KeyType": "HASH"},
            {"AttributeName": "SK", "KeyType": "RANGE"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "OrderID", "AttributeType": "N"},
            {"AttributeName": "SK", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    waiter = table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    print(table.item_count)
else:
    table = dynamodb.Table(table_name)

try:
    # Populate some data
    with table.batch_writer() as batch:
        batch.put_item(
            Item={
                "OrderID": 1,
                "SK": "shipto",
                "title": "Mrs.",
                "first_name": "Tiffani",
                "middle_initial": "D",
                "last_name": "McCorkle",
                "street": "4548 Scott Street",
                "city": "Long Island City",
                "state": "NY",
                "zip": "11101",
            }
        ),
        batch.put_item(
            Item={
                "OrderID": 1,
                "SK": "order:item#1",
                "sku": "B0791TX5P5",
                "qty": 1,
                "price": Decimal("24.99"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 1,
                "SK": "order:item#2",
                "sku": "B07PGL2N7J",
                "qty": 2,
                "price": Decimal("34.99"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 2,
                "SK": "shipto",
                "title": "Mr.",
                "first_name": "Lincoln",
                "middle_initial": "M",
                "last_name": "Maysonet",
                "street": "4276 Laurel Lee",
                "city": "Kansas City",
                "state": "MO",
                "zip": "64106",
            }
        )
        batch.put_item(
            Item={
                "OrderID": 2,
                "SK": "order:item#1",
                "sku": "1476773092",
                "qty": 2,
                "price": Decimal("16.44"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 3,
                "SK": "shipto",
                "title": "Mr.",
                "first_name": "Robert",
                "middle_initial": "D",
                "last_name": "Moxley",
                "street": "4315 Pearlman Avenue",
                "city": "Cambridge",
                "state": "MA",
                "zip": "02138",
            }
        )
        batch.put_item(
            Item={
                "OrderID": 3,
                "SK": "order:item#1",
                "sku": "B0060J3X2C",
                "qty": 1,
                "price": Decimal("128.00"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 3,
                "SK": "order:item#2",
                "sku": "B00AZQ2OF8",
                "qty": 1,
                "price": Decimal("15.00"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 3,
                "SK": "order:item#3",
                "sku": "B00AZCGF7K",
                "qty": 1,
                "price": Decimal("6.99"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 4,
                "SK": "shipto",
                "title": "Dr.",
                "first_name": "Curtis",
                "middle_initial": "B",
                "last_name": "Tucker",
                "street": "3731 Caynor Circle",
                "city": "Elizabeth",
                "state": "NJ",
                "zip": "07201",
            }
        )
        batch.put_item(
            Item={
                "OrderID": 4,
                "SK": "order:item#1",
                "sku": "B000002JPA",
                "qty": 1,
                "price": Decimal("11.94"),
            }
        )
        batch.put_item(
            Item={
                "OrderID": 5,
                "SK": "shipto",
                "title": "Ms.",
                "first_name": "Jennifer",
                "middle_initial": "J",
                "last_name": "Shaver",
                "street": "3865 Gore Street",
                "city": "Sugar Land",
                "state": "TX",
                "zip": "77478",
            }
        )
        batch.put_item(
            Item={
                "OrderID": 5,
                "SK": "order:item#1",
                "sku": "B0792FNGZW",
                "qty": 1,
                "price": Decimal("45.22"),
            }
        )

except ClientError as e:
    print(e)
else:
    print("Done.")
