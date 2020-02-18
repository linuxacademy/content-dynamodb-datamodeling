#!/bin/sh

################################################################################
# CHANGE THIS BUCKET NAME FOR YOUR ACCOUNT
S3_BUCKET=musictagger 
################################################################################

FUNCTION_NAME=MusicTagger
ROLE_NAME=$FUNCTION_NAME-Role

# Create IAM exection role

arn=$(aws iam get-role --role-name $ROLE_NAME --output text --query 'Role.Arn')

if [[ $? -eq 0 ]]; then
  echo "$ROLE_NAME exists. ARN=$arn"
else
  echo "Creating role $ROLE_NAME"
  arn=$(aws iam create-role --role-name $ROLE_NAME \
    --assume-role-policy-document file://trust-policy.json \
    --output text \
    --query 'Role.Arn')
fi

# Attach policies to role
aws iam attach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# Package Lambda function

mkdir package
pip install --target ./package mutagen
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip lambda_function.py

# Deploy Lambda function

fn_arn=$(aws lambda get-function --function-name $FUNCTION_NAME \
  --output text --query 'Configuration.FunctionArn')

if [[ $? -eq 0 ]]; then
  echo "$FUNCTION_NAME exists. ARN=$fn_arn"
  aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://function.zip
else
  echo "Creating Lambda function $FUNCTION_NAME"
  aws lambda create-function \
      --function-name $FUNCTION_NAME \
      --runtime python3.8 \
      --timeout 30 \
      --zip-file fileb://function.zip \
      --handler lambda_function.lambda_handler \
      --role $arn
fi
