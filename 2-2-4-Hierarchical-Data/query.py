#!/usr/bin/env python3

import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("TargetStores")
client = boto3.client("dynamodb")

# Get single store location

try:
    store_number = "1760"
    response = table.get_item(Key={"StoreNumber": store_number})
    print(f">>> Get item by store number found:")
    print(response["Item"])
except Exception as e:
    print("Error getting item:")
    print(e)

# Query by state

try:

    response = table.query(
        IndexName="Location-index", KeyConditionExpression=Key("State").eq("FL"),
    )
    print(f'\n>>> Query by state found {response["Count"]} locations:')
    print(response["Items"])
except Exception as e:
    print("Error running query:")
    print(e)

# Query by city

try:

    response = table.query(
        IndexName="Location-index",
        KeyConditionExpression=Key("State").eq("FL")
        & Key("StateCityPostalcode").begins_with("FL#ORLANDO"),
    )
    print(f'\n>>> Query by city found {response["Count"]} locations:')
    print(response["Items"])
except Exception as e:
    print("Error running query:")
    print(e)

# Query by postal code

try:

    response = table.query(
        IndexName="Location-index",
        KeyConditionExpression=Key("State").eq("MN")
        & Key("StateCityPostalcode").begins_with("MN#MINNEAPOLIS#55403"),
    )
    print(f'\n>>> Query by postal code found {response["Count"]} locations:')
    print(response["Items"])
except Exception as e:
    print("Error running query:")
    print(e)
