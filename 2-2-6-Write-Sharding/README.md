# 2.2.6 - Write Sharding

## Create IAM Role

Create an IAM role with the following properties:

Trusted entity – Lambda  
Permissions – `AWSLambdaDynamoDBExecutionRole`, `AmazonDynamoDBFullAccess`  
Role name – `Lambda-AggregateVotes-Role`

`AWSLambdaDynamoDBExecutionRole` provides list and read access to DynamoDB streams and write permissions to CloudWatch logs.

## Create Lambda Function

Name - `AggregateVotes`

Runtime - `Python 3.8`

Use the execution role created above.

Paste into the code editor the contents of `lambda_function.py` in this directory.

## Add CloudWatch Event

1. Add trigger to Lambda function, selecting CloudWatch Events.
2. Create new rule `AggregateVotes`
3. Set **Schedule Expression** to `rate(1 minute)`

## Populate voting data

Run `votes.py` allowing it to complete for 1000 votes.

Refresh `votes` table in DynamoDB, observing the sharded and total votes.

In the `raw_votes` table, observe unique `voter_id` values, along with timestamps, and the candidate for which the vote was cast.

