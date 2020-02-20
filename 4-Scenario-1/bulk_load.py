#!/usr/bin/env python3

import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("flights")

items = []

with open("items.json", "r") as f:
    for row in f:
        items.append(json.loads(row))

count = 0
with table.batch_writer() as batch:
    for item in items:
        if count % 1000 == 0:
            print(count)
        try:
            batch.put_item(Item=item)
        except ClientError as e:
            print(e)
        count = count + 1
