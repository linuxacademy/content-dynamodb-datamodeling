#!/usr/bin/env python3

import boto3

# This is a really inefficient (and expensive) way to truncate a table.
# You're better off deleting the table and recreating it, but I'm too
# impatient to wait for DynamoDB to create tables.

# This version takes into account the fact that you might not get all records
# back in the first call to scan() if you're trying to truncate a big table
# (or a smaller table with big items). It presumes you're only using a HashKey
# (called StoreNumber) so you'd have to add a bit to your ProjectionExpression
# and delete_item() call if you also have a sort key on your table.

table = boto3.resource("dynamodb").Table("flights")
scan = None

with table.batch_writer() as batch:
    count = 0
    while scan is None or "LastEvaluatedKey" in scan:
        if scan is not None and "LastEvaluatedKey" in scan:
            scan = table.scan(ExclusiveStartKey=scan["LastEvaluatedKey"],)
        else:
            scan = table.scan()

        for item in scan["Items"]:
            if count % 100 == 0:
                print(count)
            batch.delete_item(Key={"PK": item["PK"], "SK": item["SK"]})
            count = count + 1
