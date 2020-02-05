#!/usr/bin/env python3

import time

import boto3
from boto3.dynamodb.conditions import Attr, Key

table = boto3.resource("dynamodb").Table("Inventory")
index_name = "Data-index"

# When adding a GSI to an existing table, you can't query the index until it
# has been backfilled. This portion of the script waits until the index is in
# the "ACTIVE" status, indicating it is ready to be queried.

while True:
    if (
        not table.global_secondary_indexes
        or table.global_secondary_indexes[0]["IndexStatus"] != "ACTIVE"
    ):
        print("Waiting for index to backfill...")
        time.sleep(5)
        table.reload()
    else:
        break

# When making a Query call, you use the KeyConditionExpression parameter to
# specify the partition key on which you want to query. If you want to use a
# specific index, you also need to pass the IndexName in your API call.

# Query our access patterns:
# - Find all orders for a user within the last 30 days.
# - For a given warehouse, which parts are on backorder?

# print(">>> Find all orders for a user within the last 30 days.\n")
# resp = table.query(
#     IndexName=index_name,
#     KeyConditionExpression=Key("SK").eq("USER#1234"),
#     FilterExpression=Attr("ID").begins_with("ORDER#")
#     & Attr("OrderDate").gt("2019-12-01"),
# )
# for item in resp["Items"]:
#     print(item)

print("\n>>> For a given warehouse, which parts are on backorder?\n")
resp = table.query(
    IndexName=index_name,
    KeyConditionExpression=Key("SK").eq("WH#63") & Key("Data").eq("Backordered"),
)
for item in resp["Items"]:
    print(item)
