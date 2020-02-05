#!/usr/bin/env python3

import boto3

# This is a really inefficient (and expensive) way to truncate a table.
# You're better off deleting the table and recreating it, but I'm too
# impatient to wait for DynamoDB to create tables.

table = boto3.resource("dynamodb").Table("Orders-SparseIndex")

response = table.scan()

with table.batch_writer() as batch:
    for item in response["Items"]:
        batch.delete_item(
            Key={"CustomerID": item["CustomerID"], "OrderID": item["OrderID"]}
        )
