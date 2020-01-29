#!/usr/bin/env python3

import time

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("Projects")

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

print(">>> Get all employees by project ID\n")
resp = table.query(
    KeyConditionExpression=Key("ID").eq("PROJECT1")
    & Key("Item").begins_with("EMPLOYEE"),
)
for item in resp["Items"]:
    print(item)

print("\n>>> Get all projects by employee ID\n")
resp = table.query(
    IndexName="Item-index",
    KeyConditionExpression=Key("Item").eq("EMPLOYEE2"),
    FilterExpression=Key("ID").begins_with("PROJECT"),
)
for item in resp["Items"]:
    print(item)
