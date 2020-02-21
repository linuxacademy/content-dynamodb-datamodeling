#!/usr/bin/env python3

"""Bulk load flights table with data"""

import csv
import json

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("flights")
airlines = {}
airports = {}
planes = {}


def load_airlines():
    with open("airlines.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3]:
                airlines[row[3]] = row[1]


def load_airports():
    with open("airports.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[4]:
                airports[row[4]] = row[1]


def load_planes():
    with open("planes.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            planes[row[1]] = row[0]


def format_item(item):
    data = {}
    data["PK"] = item[2]  # source airport code
    data["SK"] = item[4]  # destination airport code
    if airports.get(item[2]):
        data["src_ap"] = airports.get(item[2])
    if airports.get(item[4]):
        data["dst_ap"] = airports.get(item[4])
    if planes.get(item[8]):
        data["plane"] = planes.get(item[8])
    if item[8]:
        data["plane_iata"] = item[8]
    return data


def generate_json():
    print("Generating bulk load data...")
    load_airlines()
    load_airports()
    load_planes()

    tuple_dict = {}

    with open("routes.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers

        for row in reader:
            item = format_item(row)
            tuple_dict[(item["PK"], item["SK"])] = item

        with open("items.json", mode="w") as outfile:
            for v in tuple_dict.values():
                item = json.dumps(v)
                outfile.write(f"{item}\n")


if __name__ == "__main__":
    generate_json()

    print("Loading flights table...")

    items = []

    with open("items.json", "r") as f:
        for row in f:
            items.append(json.loads(row))

    count = 0
    with table.batch_writer() as batch:
        for item in items:
            if count % 1000 == 0:
                print(f"Wrote {count} items")
            try:
                batch.put_item(Item=item)
            except ClientError as e:
                print(e)
            count = count + 1
