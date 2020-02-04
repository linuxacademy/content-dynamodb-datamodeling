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

Use `lambda_function.py` in this directory.
