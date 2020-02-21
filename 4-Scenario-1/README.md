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
