#!/usr/bin/env python3

"""Update employees table using parallel scan"""
import datetime
import threading

import boto3
from botocore.exceptions import ClientError

MAX_THREADS = 100
TABLE_NAME = "employees"
dynamodb = boto3.resource("dynamodb")
client = boto3.client("dynamodb")
table = dynamodb.Table(TABLE_NAME)
thirty_years_ago = (
    datetime.datetime.now() - datetime.timedelta(days=30 * 365)
).strftime("%Y-%m-%d")


def scan_table(segment, total_segments):
    scan = None
    print(f"Scanning segment {segment}")
    try:
        while scan is None or "LastEvaluatedKey" in scan:
            if scan is not None and "LastEvaluatedKey" in scan:
                scan = table.scan(
                    TableName=TABLE_NAME,
                    Segment=segment,
                    TotalSegments=total_segments,
                    ExclusiveStartKey=scan["LastEvaluatedKey"],
                )
            else:
                scan = table.scan(
                    TableName=TABLE_NAME, Segment=segment, TotalSegments=total_segments,
                )

            count = len(scan["Items"])
            print(f"Segment {segment} returned {count} items")

            for item in scan["Items"]:
                if (
                    item["salary_to_date"] == "9999-01-01"
                    and item["hire_date"] <= thirty_years_ago
                ):
                    print(
                        f"Hire date: {item['hire_date']}, updating emp_no {item['emp_no']}"
                    )
                    response = table.update_item(
                        Key={"emp_no": item["emp_no"], "salary": item["salary"]},
                        UpdateExpression="ADD is_current :c",
                        ExpressionAttributeValues={":c": 1},
                        ReturnValues="ALL_NEW",
                    )
                    print(response)

    except ClientError as e:
        print(e)


def create_threads():
    threads = []

    for i in range(MAX_THREADS):
        thread = threading.Thread(target=scan_table, args=(i, MAX_THREADS))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    create_threads()
