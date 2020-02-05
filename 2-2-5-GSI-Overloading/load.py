#!/usr/bin/env python3

import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table("Inventory")

try:
    with table.batch_writer() as batch:
        batch.put_item(Item={"ID": "USER#1234", "SK": "Richman, Mark"}),
        batch.put_item(
            Item={
                "ID": "ORDER#9877",
                "SK": "USER#1234",
                "Data": "149.99",
                "OrderDate": "2020-01-04",
            }
        ),
        batch.put_item(Item={"ID": "WH#63", "SK": "FL#ORLANDO"}),
        batch.put_item(
            Item={
                "ID": "PART#8823",
                "SK": "WH#63",
                "Data": "Backordered",
                "PartName": "Flux Capacitor",
            }
        )
        batch.put_item(Item={"ID": "USER#1066", "SK": "Cox, Terry"}),
        batch.put_item(
            Item={
                "ID": "ORDER#9921",
                "SK": "USER#1066",
                "Data": "275.49",
                "OrderDate": "2020-02-02",
            }
        ),
        batch.put_item(Item={"ID": "WH#24", "SK": "TX#DALLAS"}),
        batch.put_item(
            Item={
                "ID": "PART#8762",
                "SK": "WH#24",
                "Data": "In Stock",
                "PartName": "Warp Coil",
            }
        ),
        batch.put_item(
            Item={
                "ID": "PART#8829",
                "SK": "WH#63",
                "Data": "Backordered",
                "PartName": "Tachyon Emitter",
            }
        )
except ClientError as e:
    print(e)
