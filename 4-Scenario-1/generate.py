#!/usr/bin/env python3

import csv
import json


def load_airlines():
    airlines = {}
    with open("airlines.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[3]:
                airlines[row[3]] = row[1]
    return airlines


def load_airports():
    airports = {}
    with open("airports.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[4]:
                airports[row[4]] = row[1]
    return airports


def load_planes():
    planes = {}
    with open("planes.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            planes[row[1]] = row[0]
    return planes


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


if __name__ == "__main__":
    airlines = load_airlines()
    airports = load_airports()
    planes = load_planes()

    tuple_dict = {}

    with open("routes.csv", mode="r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers

        for row in reader:
            item = format_item(row)
            tuple_dict[(item["PK"], item["SK"])] = item

        with open("items.json", mode="a") as outfile:
            for v in tuple_dict.values():
                item = json.dumps(v)
                outfile.write(f"{item}\n")
