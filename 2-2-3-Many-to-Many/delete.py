#!/usr/bin/env python3

import boto3

# This is a really inefficient (and expensive) way to truncate a table.
# You're better off deleting the table and recreating it, but I'm too
# impatient to wait for DynamoDB to create tables.

table = boto3.resource("dynamodb").Table("Projects")

response = table.scan()

for item in response["Items"]:
    table.delete_item(Key={"ID": item["ID"], "Item": item["Item"]})
