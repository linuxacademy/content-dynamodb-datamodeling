#!/usr/bin/env python3

import boto3
from boto3.dynamodb.conditions import Key

client = boto3.client("dynamodb")
order_table = boto3.resource("dynamodb").Table("Orders")

print(">>> QUERY OrderID = 2, SK = 'shipto'\n")
response = order_table.query(
    KeyConditionExpression=Key("OrderID").eq(2) & Key("SK").eq("shipto")
)
print(response["Items"])

print("\n>>> QUERY OrderID = 3, SK.begins_with('order:item')\n")
response = order_table.query(
    KeyConditionExpression=Key("OrderID").eq(3) & Key("SK").begins_with("order:item")
)
print(response["Items"])

print("\n>>> QUERY OrderID = 5\n")
response = order_table.query(KeyConditionExpression=Key("OrderID").eq(5))
print(response["Items"])
