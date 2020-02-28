#!/usr/bin/env python3

from pprint import pprint

import boto3
from boto3.dynamodb.conditions import Attr, Key

table = boto3.resource("dynamodb").Table("employees")

"""
Access Patterns:
1. Find employee by employee ID
2. Find all employees for a given last name
3. Find all employees for a given title
4. Find all employees for a given department
5. Find all employees with salary >= 130,000
6. Find all current department managers
"""

input("\n>>> [AP1] Find employee by employee ID (press enter):\n")
resp = table.query(
    KeyConditionExpression=Key("emp_no").eq(485395),
    FilterExpression=Attr("salary_to_date").eq("9999-01-01"),
)
for item in resp["Items"]:
    pprint(item)

input("\n>>> [AP2] Find all employees for a given last name (press enter):\n")
resp = table.query(
    IndexName="last_name-index",
    KeyConditionExpression=Key("last_name").eq("Weedman"),
    FilterExpression=Attr("salary_to_date").eq("9999-01-01"),
)
for item in resp["Items"]:
    pprint(item)

print(f"Found {len(resp['Items'])} items.")

input("\n>>> [AP3] Find all employees for a given title (press enter):\n")
resp = table.query(
    IndexName="title-index",
    KeyConditionExpression=Key("title").eq("Senior Engineer"),
    FilterExpression=Attr("salary_to_date").eq("9999-01-01"),
)
for item in resp["Items"]:
    pprint(item)

print(f"Found {len(resp['Items'])} items.")

input("\n>>> [AP4] Find all employees for a given department (press enter):\n")
resp = table.query(
    IndexName="department_name-index",
    KeyConditionExpression=Key("department_name").eq("Finance"),
    FilterExpression=Attr("salary_to_date").eq("9999-01-01"),
)
for item in resp["Items"]:
    pprint(item)

print(f"Found {len(resp['Items'])} items.")

input("\n>>> [AP5] Find all employees with salary >= 130,000 (press enter):\n")
resp = table.query(
    IndexName="salary-index",
    KeyConditionExpression=Key("salary_to_date").eq("9999-01-01")
    & Key("salary").gte(130000),
)
for item in resp["Items"]:
    pprint(item)

print(f"Found {len(resp['Items'])} items.")

input("\n>>> [AP6] Find all current department managers (press enter):\n")

depts = [
    "Customer Service",
    "Development",
    "Finance",
    "Human Resources",
    "Marketing",
    "Production",
    "Quality Management",
    "Research",
    "Sales",
]

mgrs = []

for dept in depts:
    resp = table.query(
        IndexName="department_manager-index",
        KeyConditionExpression=Key("department_name").eq(dept),
        Limit=1,
    )
    mgrs.append(resp["Items"][0])

pprint(mgrs)
print(f"Found {len(mgrs)} items.")
