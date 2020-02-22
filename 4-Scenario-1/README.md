# Scenario 1: Flight Information Microservice

## Deploy SAM Application

The SAM template in `flights-app` will create the DynamoDB table, and deploy the API Gateway endpoints and Lambda functions required for this lesson.

Install the AWS SAM CLI: <https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html>

```sh
cd flights-app
sam build
sam deploy --guided
```

## Extract data files

```sh
gunzip *.gz
```

## Generate and bulk load data into DynamoDB

```sh
./load.py
```

## Access Patterns

1. Find flight by source and destination airport code
1. Find airport name by airport code
1. Find airport code by airport name
1. Find all flights using a specific plane
1. Find all flights outbound from an airport code

## GSIs

1. src_ap-index
2. plane_iata-index

## Testing

Once the `flights-app` SAM application has been deployed, and the data has been loaded into DynamoDB, you may test the APIs using `test.sh`. The output will appear as follows:

```text
>>> Finding flights by plane

{"count": 10, "data": [{"plane_iata": "747", "SK": "AMS", "plane": "Boeing 747", "src_ap": "San Francisco International Airport", "PK": "SFO", "dst_ap": "Amsterdam Airport Schiphol"}, {"plane_iata": "747", "SK": "CUR", "plane": "Boeing 747", "src_ap": "Princess Juliana International Airport", "PK": "SXM", "dst_ap": "Hato International Airport"}, {"plane_iata": "747", "SK": "RUN", "plane": "Boeing 747", "src_ap": "Paris-Orly Airport", "PK": "ORY", "dst_ap": "Roland Garros Airport"}, {"plane_iata": "747", "SK": "SFO", "plane": "Boeing 747", "src_ap": "Amsterdam Airport Schiphol", "PK": "AMS", "dst_ap": "San Francisco International Airport"}, {"plane_iata": "747", "SK": "BKK", "plane": "Boeing 747", "src_ap": "Sydney Kingsford Smith International Airport", "PK": "SYD", "dst_ap": "Suvarnabhumi Airport"}, {"plane_iata": "747", "SK": "SYD", "plane": "Boeing 747", "src_ap": "Suvarnabhumi Airport", "PK": "BKK", "dst_ap": "Sydney Kingsford Smith International Airport"}, {"plane_iata": "747", "SK": "SXM", "plane": "Boeing 747", "src_ap": "Amsterdam Airport Schiphol", "PK": "AMS", "dst_ap": "Princess Juliana International Airport"}, {"plane_iata": "747", "SK": "BKK", "plane": "Boeing 747", "src_ap": "Munich International Airport", "PK": "MUC", "dst_ap": "Suvarnabhumi Airport"}, {"plane_iata": "747", "SK": "MUC", "plane": "Boeing 747", "src_ap": "Suvarnabhumi Airport", "PK": "BKK", "dst_ap": "Munich International Airport"}, {"plane_iata": "747", "SK": "ORY", "plane": "Boeing 747", "src_ap": "Roland Garros Airport", "PK": "RUN", "dst_ap": "Paris-Orly Airport"}]}

>>> Finding airport by code

"Orlando International Airport"

>>> Finding airport by name

"MCO"

>>> Finding flights by codes

{"plane_iata": "SF3", "SK": "FLL", "plane": "Saab SF340A/B", "src_ap": "Orlando International Airport", "PK": "MCO", "dst_ap": "Fort Lauderdale Hollywood International Airport"}

>>> Finding outbound flights by airport

{"plane_iata": "320", "SK": "ACY", "plane": "Airbus A320", "src_ap": "Orlando International Airport", "PK": "MCO", "dst_ap": "Atlantic City International Airport"}
```

Explore the results by altering the various querystring parameters in `test.sh`.
