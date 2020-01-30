#!/usr/bin/env python3

import csv

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("TargetStores")


def format_item(row):
    item = {}
    item["City"] = row["Address.City"]
    item["Country"] = row["Address.CountryName"]
    item["Latitude"] = row["Address.Latitude"]
    item["Longitude"] = row["Address.Longitude"]
    item["PhoneNumber"] = row["PhoneNumber"]
    item["PostalCode"] = row["Address.PostalCode"]
    item["State"] = row["Address.Subdivision"]
    item["StateCityPostalcode"] = "{state}#{city}#{postalcode}".format(
        state=row["Address.Subdivision"].upper(),
        city=row["Address.City"].upper(),
        postalcode=row["Address.PostalCode"].upper().split("-")[0],
    )
    item["StoreName"] = row["Name"]
    item["StoreNumber"] = row["ID"]
    item["StreetAddress"] = row["Address.FormattedAddress"]

    return item


if __name__ == "__main__":
    count = 0
    with table.batch_writer() as batch:
        with open("target.csv", "r", encoding="ISO-8859-1") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = format_item(row)
                batch.put_item(Item=item)
                count += 1
                if count % 100 == 0:
                    print(f"{count} items written...")
